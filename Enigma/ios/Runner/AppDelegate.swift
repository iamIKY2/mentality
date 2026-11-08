import Flutter
import UIKit
import UserNotifications

@main
@objc class AppDelegate: FlutterAppDelegate, FlutterImplicitEngineDelegate {
  private var configurationChannel: FlutterMethodChannel?
  override func application(
    _ application: UIApplication,
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?
  ) -> Bool {
    UNUserNotificationCenter.current().delegate = self
    return super.application(application, didFinishLaunchingWithOptions: launchOptions)
  }

  func didInitializeImplicitFlutterEngine(_ engineBridge: FlutterImplicitEngineBridge) {
    GeneratedPluginRegistrant.register(with: engineBridge.pluginRegistry)
    if let registrar = engineBridge.pluginRegistry.registrar(forPlugin: "EnigmaIOSConfiguration") {
      let channel = FlutterMethodChannel(
        name: "enigma/ios_configuration",
        binaryMessenger: registrar.messenger()
      )
      channel.setMethodCallHandler { call, result in
        guard call.method == "isGoogleSignInConfigured" else {
          result(FlutterMethodNotImplemented)
          return
        }
        let bundle = Bundle.main
        var clientID = bundle.object(forInfoDictionaryKey: "GIDClientID") as? String
        if clientID == nil,
           let path = bundle.path(forResource: "GoogleService-Info", ofType: "plist"),
           let info = NSDictionary(contentsOfFile: path) {
          clientID = info["CLIENT_ID"] as? String
        }
        guard let clientID = clientID, clientID.hasSuffix(".apps.googleusercontent.com") else {
          result(false)
          return
        }
        let callbackScheme = clientID.components(separatedBy: ".").reversed().joined(separator: ".")
        let urlTypes = bundle.object(forInfoDictionaryKey: "CFBundleURLTypes") as? [[String: Any]] ?? []
        let schemes = urlTypes.flatMap { $0["CFBundleURLSchemes"] as? [String] ?? [] }
        result(schemes.contains(callbackScheme))
      }
      configurationChannel = channel
    }
  }
}
