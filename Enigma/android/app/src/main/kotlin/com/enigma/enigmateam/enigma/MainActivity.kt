package com.enigma.enigmateam.enigma

import android.app.AppOpsManager
import android.app.usage.UsageEvents
import android.app.usage.UsageStatsManager
import android.content.ActivityNotFoundException
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.BatteryManager
import android.os.Build
import android.os.Process
import android.provider.Settings
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(
            flutterEngine.dartExecutor.binaryMessenger,
            "com.enigma.enigmateam.enigma/sleep_sensor"
        ).setMethodCallHandler { call, result ->
            try {
                when (call.method) {
                    "isUsagePermissionGranted" -> result.success(hasUsagePermission())
                    "requestUsagePermission" -> result.success(openUsageSettings())
                    "getScreenEvents" -> result.success(
                        getScreenEvents(call.argument<Int>("hours") ?: 24)
                    )
                    "getChargingState" -> {
                        val battery = registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
                        val status = battery?.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
                        result.success(mapOf("isCharging" to (
                            status == BatteryManager.BATTERY_STATUS_CHARGING ||
                                status == BatteryManager.BATTERY_STATUS_FULL
                        )))
                    }
                    else -> result.notImplemented()
                }
            } catch (exception: Exception) {
                result.error("SLEEP_SENSOR_ERROR", exception.message, null)
            }
        }
    }

    private fun hasUsagePermission(): Boolean {
        val appOps = getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager
        val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            appOps.unsafeCheckOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), packageName)
        } else {
            @Suppress("DEPRECATION")
            appOps.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), packageName)
        }
        return mode == AppOpsManager.MODE_ALLOWED
    }

    private fun openUsageSettings(): Boolean {
        // Prefer this app's page; some manufacturers only support the full list.
        val intents = listOf(
            Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS, Uri.parse("package:$packageName")),
            Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
        )
        for (intent in intents) {
            try {
                startActivity(intent)
                return true
            } catch (_: ActivityNotFoundException) {
                // Try the next supported settings route.
            } catch (_: SecurityException) {
                // The manufacturer may restrict the app-specific route.
            }
        }
        return false
    }

    private fun getScreenEvents(hours: Int): List<Map<String, Any>> {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.P || !hasUsagePermission()) {
            return emptyList()
        }
        val manager = getSystemService(Context.USAGE_STATS_SERVICE) as UsageStatsManager
        val end = System.currentTimeMillis()
        val start = end - hours.coerceIn(1, 168) * 60L * 60L * 1000L
        val events = manager.queryEvents(start, end) ?: return emptyList()
        val event = UsageEvents.Event()
        val screenEvents = mutableListOf<Map<String, Any>>()
        while (events.hasNextEvent()) {
            events.getNextEvent(event)
            val type = when (event.eventType) {
                UsageEvents.Event.SCREEN_INTERACTIVE -> "SCREEN_INTERACTIVE"
                UsageEvents.Event.SCREEN_NON_INTERACTIVE -> "SCREEN_NON_INTERACTIVE"
                UsageEvents.Event.KEYGUARD_SHOWN -> "KEYGUARD_SHOWN"
                UsageEvents.Event.KEYGUARD_HIDDEN -> "KEYGUARD_HIDDEN"
                else -> continue
            }
            screenEvents.add(mapOf("type" to type, "timestamp" to event.timeStamp))
        }
        return screenEvents
    }
}
