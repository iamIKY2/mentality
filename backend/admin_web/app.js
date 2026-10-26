/**
 * ==============================================================================
 * ENIGMA ADMIN PORTAL — JAVASCRIPT APPLICATION CORE
 * ==============================================================================
 * Hệ sinh thái Quản trị Sức khỏe & Thích nghi Thực tập sinh Enigma
 * - Quản lý sinh viên & chỉ số 5 trụ cột
 * - Trung tâm phát hiện & can thiệp nguy cơ kiệt sức (Burnout Alert)
 * - Quản lý cẩm nang RAG AI & Nhiệm vụ 3 giai đoạn
 * - Tự động kết nối Live FastAPI (8000) hoặc chế độ Demo Data mượt mà
 */

(function () {
  'use strict';

  // URL Máy chủ Render Cloud Production của ứng dụng Enigma
  const RENDER_CLOUD_URL = 'https://mentality-38jh.onrender.com';

  function getInitialApiUrl() {
    // Tự động nhận diện thông minh 100%:
    // - Khi mở trên http://localhost:8000/admin-web/ -> Tự gọi http://localhost:8000
    // - Khi mở trên https://mentality-38jh.onrender.com/admin-web/ -> Tự gọi https://mentality-38jh.onrender.com
    if (window.location.origin && window.location.origin !== 'null' && !window.location.origin.startsWith('file:')) {
      return window.location.origin;
    }
    const saved = localStorage.getItem('enigma_api_url');
    if (saved) return saved;
    return RENDER_CLOUD_URL;
  }

  // ─── Application State ────────────────────────────────────────────────────────
  const STATE = {
    apiBaseUrl: getInitialApiUrl(),
    adminToken: localStorage.getItem('enigma_admin_token') || 'enigma_admin_master_secret',
    isDemoMode: false,
    activeTab: 'dashboard',
    activeTaskPhase: 'preparation',
    
    // Data Caches
    stats: null,
    students: [],
    alerts: [],
    articles: [],
    tasks: [],
    notifications: [],

    // Chart instances
    charts: {
      pillars: null,
      stress: null,
      trend: null,
    }
  };

  // ─── DOM References ───────────────────────────────────────────────────────────
  const DOM = {
    // Navigation
    navItems: document.querySelectorAll('.nav-item'),
    tabPanes: document.querySelectorAll('.tab-pane'),
    pageTitle: document.getElementById('page-title'),
    pageSubtitle: document.getElementById('page-subtitle'),
    connectionPill: document.getElementById('connection-pill'),
    statusIndicator: document.getElementById('status-indicator'),
    statusLabel: document.getElementById('status-label'),
    toggleDataModeBtn: document.getElementById('toggle-data-mode-btn'),
    btnRefresh: document.getElementById('btn-refresh'),
    btnQuickBroadcast: document.getElementById('btn-quick-broadcast'),
    mobileMenuBtn: document.getElementById('mobile-menu-btn'),
    sidebar: document.getElementById('sidebar'),

    // Badges
    navBadgeStudents: document.getElementById('nav-badge-students'),
    navBadgeAlerts: document.getElementById('nav-badge-alerts'),
    navBadgeArticles: document.getElementById('nav-badge-articles'),
    quickAlertCount: document.getElementById('quick-alert-count'),

    // KPI Values
    kpiTotalStudents: document.getElementById('kpi-total-students'),
    kpiCheckinsToday: document.getElementById('kpi-checkins-today'),
    kpiCheckinRate: document.getElementById('kpi-checkin-rate'),
    kpiBurnoutRisk: document.getElementById('kpi-burnout-risk'),
    kpiCompletedTasks: document.getElementById('kpi-completed-tasks'),

    // Dashboard Lists
    dashboardFeedList: document.getElementById('dashboard-feed-list'),
    dashboardWatchlist: document.getElementById('dashboard-watchlist'),

    // Students Directory
    studentsSearchInput: document.getElementById('students-search-input'),
    studentsFilterPhase: document.getElementById('students-filter-phase'),
    studentsFilterRisk: document.getElementById('students-filter-risk'),
    studentsTbody: document.getElementById('students-tbody'),
    btnExportStudents: document.getElementById('btn-export-students'),

    // Burnout Alert Center
    burnoutCardsContainer: document.getElementById('burnout-cards-container'),

    // Handbook
    handbookSearchInput: document.getElementById('handbook-search-input'),
    handbookFilterCategory: document.getElementById('handbook-filter-category'),
    handbookFilterStatus: document.getElementById('handbook-filter-status'),
    handbookArticlesContainer: document.getElementById('handbook-articles-container'),
    btnCreateArticle: document.getElementById('btn-create-article'),

    // Tasks
    taskPhaseSwitcher: document.getElementById('task-phase-switcher'),
    tasksTbody: document.getElementById('tasks-tbody'),
    btnCreateTask: document.getElementById('btn-create-task'),

    // Broadcast
    broadcastForm: document.getElementById('broadcast-form'),
    notificationHistoryList: document.getElementById('notification-history-list'),

    // Settings
    settingApiUrl: document.getElementById('setting-api-url'),
    settingAdminToken: document.getElementById('setting-admin-token'),
    btnSaveSettings: document.getElementById('btn-save-settings'),
    btnTestConnection: document.getElementById('btn-test-connection'),
    btnExportJson: document.getElementById('btn-export-json'),
    btnClearCache: document.getElementById('btn-clear-cache'),

    // Modals
    userModal: document.getElementById('user-modal'),
    articleModal: document.getElementById('article-modal'),
    articleForm: document.getElementById('article-form'),
    taskModal: document.getElementById('task-modal'),
    taskForm: document.getElementById('task-form'),

    // Toast
    toastContainer: document.getElementById('toast-container'),
  };

  // ─── Toast System ─────────────────────────────────────────────────────────────
  function showToast(message, type = 'info', duration = 3500) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let iconSvg = '';
    if (type === 'success') {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
    } else if (type === 'error') {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';
    } else {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
    }

    toast.innerHTML = `${iconSvg}<span>${message}</span>`;
    DOM.toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  }

  // ─── Tab Title Dictionary ─────────────────────────────────────────────────────
  const TAB_TITLES = {
    dashboard: {
      title: 'Tổng Quan Dashboard',
      subtitle: 'Theo dõi trạng thái 5 trụ cột sức khỏe và rủi ro kiệt sức của thực tập sinh',
    },
    students: {
      title: 'Quản Lý Sinh Viên Thực Tập',
      subtitle: 'Danh bạ sinh viên, phân loại theo doanh nghiệp, giai đoạn và chỉ số sức khỏe',
    },
    burnout: {
      title: 'Trung Tâm Cảnh Báo Kiệt Sức',
      subtitle: 'Sàng lọc nguy cơ stress cao, thiếu ngủ ca đêm và đưa ra can thiệp kịp thời',
    },
    handbook: {
      title: 'Cẩm Nang Thực Tập & Huấn Luyện AI RAG',
      subtitle: 'Kho tri thức kinh nghiệm cựu sinh viên, phân loại 5 trụ cột và vector hóa',
    },
    tasks: {
      title: 'Nhiệm Vụ Thích Nghi 3 Giai Đoạn',
      subtitle: 'Lộ trình phát triển: Chuẩn bị ➔ Hòa nhập doanh nghiệp ➔ Duy trì & Bứt phá',
    },
    notifications: {
      title: 'Trung Tâm Phát Loa & Thông Báo',
      subtitle: 'Gửi lời nhắc nhở sinh hoạt, Gacha quotes và thông báo khẩn tới ứng dụng sinh viên',
    },
    settings: {
      title: 'Cấu Hình Hệ Thống & Kết Nối API',
      subtitle: 'Cài đặt máy chủ Backend, mã token quản trị và xuất dữ liệu báo cáo',
    },
  };

  // ─── Tab Switching ────────────────────────────────────────────────────────────
  function switchTab(tabName) {
    if (!TAB_TITLES[tabName]) return;
    STATE.activeTab = tabName;

    DOM.navItems.forEach(item => {
      item.classList.toggle('active', item.dataset.tab === tabName);
    });

    DOM.tabPanes.forEach(pane => {
      pane.classList.toggle('active', pane.id === `pane-${tabName}`);
    });

    DOM.pageTitle.textContent = TAB_TITLES[tabName].title;
    DOM.pageSubtitle.textContent = TAB_TITLES[tabName].subtitle;

    // Render tab content on switch if needed
    if (tabName === 'dashboard') {
      renderDashboardCharts();
    } else if (tabName === 'students') {
      renderStudentsTable();
    } else if (tabName === 'burnout') {
      renderBurnoutCards();
    } else if (tabName === 'handbook') {
      renderHandbookArticles();
    } else if (tabName === 'tasks') {
      renderTasksTable();
    } else if (tabName === 'notifications') {
      renderNotificationHistory();
    }

    // Close mobile sidebar
    DOM.sidebar.classList.remove('mobile-open');
  }

  // ─── Rich Mock / Demo Data Generator ──────────────────────────────────────────
  function getMockData() {
    const mockStudents = [
      {
        id: "sv-101",
        student_id: "B21DCCN045",
        full_name: "Nguyễn Minh Khang",
        email: "khang.nm@ptit.edu.vn",
        university: "Học viện CNBCVT",
        major: "Công nghệ thông tin",
        company_name: "LG Display Hải Phòng",
        department: "Kỹ thuật Module Màn hình",
        current_phase: "adaptation",
        current_streak: 14,
        latest_stress_level: 2,
        latest_sleep_hours: 7.5,
        is_high_risk: false,
        is_active: true,
        role: "student",
        initial_scores: { sleep: 75, physical: 80, mental: 70, social: 85, career: 90 },
        created_at: "2026-09-01T08:00:00Z"
      },
      {
        id: "sv-102",
        student_id: "B21DCCN189",
        full_name: "Trần Thị Thùy Linh",
        email: "linh.ttt@hust.edu.vn",
        university: "ĐH Bách Khoa Hà Nội",
        major: "Kỹ thuật Điện tử",
        company_name: "LG Display Hải Phòng",
        department: "Chất lượng sản phẩm (QA)",
        current_phase: "adaptation",
        current_streak: 8,
        latest_stress_level: 5,
        latest_sleep_hours: 4.2,
        is_high_risk: true,
        is_active: true,
        role: "student",
        initial_scores: { sleep: 50, physical: 60, mental: 45, social: 65, career: 70 },
        created_at: "2026-09-05T09:30:00Z"
      },
      {
        id: "sv-103",
        student_id: "B21DCCN312",
        full_name: "Lê Hoàng Long",
        email: "long.lh@utc.edu.vn",
        university: "ĐH Giao Thông Vận Tải",
        major: "Kỹ thuật Cơ điện tử",
        company_name: "LG Display Hải Phòng",
        department: "Bảo trì Thiết bị ESD",
        current_phase: "preparation",
        current_streak: 21,
        latest_stress_level: 1,
        latest_sleep_hours: 8.0,
        is_high_risk: false,
        is_active: true,
        role: "student",
        initial_scores: { sleep: 85, physical: 85, mental: 80, social: 75, career: 80 },
        created_at: "2026-09-10T10:15:00Z"
      },
      {
        id: "sv-104",
        student_id: "B21DCCN408",
        full_name: "Phạm Quốc Tuấn",
        email: "tuan.pq@hust.edu.vn",
        university: "ĐH Bách Khoa Hà Nội",
        major: "Tự động hóa",
        company_name: "LG Display Hải Phòng",
        department: "Dây chuyền Cleanroom ca đêm",
        current_phase: "adaptation",
        current_streak: 4,
        latest_stress_level: 4,
        latest_sleep_hours: 4.8,
        is_high_risk: true,
        is_active: true,
        role: "student",
        initial_scores: { sleep: 55, physical: 65, mental: 50, social: 60, career: 75 },
        created_at: "2026-09-12T14:20:00Z"
      },
      {
        id: "sv-105",
        student_id: "B21DCCN512",
        full_name: "Hoàng Thảo My",
        email: "my.ht@neu.edu.vn",
        university: "ĐH Kinh Tế Quốc Dân",
        major: "Quản trị Nhân lực",
        company_name: "LG Display Hải Phòng",
        department: "Phòng Nhân sự Thực tập sinh",
        current_phase: "sustain",
        current_streak: 30,
        latest_stress_level: 2,
        latest_sleep_hours: 7.0,
        is_high_risk: false,
        is_active: true,
        role: "student",
        initial_scores: { sleep: 70, physical: 75, mental: 75, social: 90, career: 85 },
        created_at: "2026-08-20T11:00:00Z"
      },
      {
        id: "sv-106",
        student_id: "B21DCCN620",
        full_name: "Đặng Quang Huy",
        email: "huy.dq@phenikaa.edu.vn",
        university: "ĐH Phenikaa",
        major: "Kỹ thuật Điều khiển",
        company_name: "LG Display Hải Phòng",
        department: "Vận hành máy tự động",
        current_phase: "adaptation",
        current_streak: 2,
        latest_stress_level: 4,
        latest_sleep_hours: 5.2,
        is_high_risk: true,
        is_active: true,
        role: "student",
        initial_scores: { sleep: 60, physical: 60, mental: 55, social: 70, career: 70 },
        created_at: "2026-09-18T16:45:00Z"
      }
    ];

    const mockAlerts = [
      {
        journal_id: "j-001",
        user_id: "sv-102",
        full_name: "Trần Thị Thùy Linh",
        student_id: "B21DCCN189",
        email: "linh.ttt@hust.edu.vn",
        company_name: "LG Display Hải Phòng",
        department: "Chất lượng sản phẩm (QA)",
        current_phase: "adaptation",
        journal_date: new Date().toISOString().split('T')[0],
        stress_level: 5,
        sleep_hours: 4.2,
        physical_symptoms: ["Đau đầu", "Chóng mặt", "Mỏi mắt phòng sạch"],
        note: "Hôm qua ca đêm đổi ca đột ngột, tiếng ồn ký túc xá khiến mình không ngủ được, vào ca hoa mắt suýt làm rơi mẫu kính.",
        ai_sentiment: "very_negative",
        risk_level: "critical",
        intervention_recommended: "Cần cố vấn tâm lý gọi điện can thiệp và hỗ trợ chuyển phòng ký túc xá yên tĩnh."
      },
      {
        journal_id: "j-002",
        user_id: "sv-104",
        full_name: "Phạm Quốc Tuấn",
        student_id: "B21DCCN408",
        email: "tuan.pq@hust.edu.vn",
        company_name: "LG Display Hải Phòng",
        department: "Dây chuyền Cleanroom ca đêm",
        current_phase: "adaptation",
        journal_date: new Date().toISOString().split('T')[0],
        stress_level: 4,
        sleep_hours: 4.8,
        physical_symptoms: ["Đau khớp cổ chân", "Căng cơ vai gáy"],
        note: "Đứng giày chống tĩnh điện ESD 12 tiếng liên tục gan bàn chân sưng tấy, không biết có chịu nổi hết tuần không.",
        ai_sentiment: "negative",
        risk_level: "warning",
        intervention_recommended: "Gợi ý cẩm nang lót giày y tế silicon và bài tập ngâm chân nước ấm giảm phù nề."
      },
      {
        journal_id: "j-003",
        user_id: "sv-106",
        full_name: "Đặng Quang Huy",
        student_id: "B21DCCN620",
        email: "huy.dq@phenikaa.edu.vn",
        company_name: "LG Display Hải Phòng",
        department: "Vận hành máy tự động",
        current_phase: "adaptation",
        journal_date: new Date(Date.now() - 86400000).toISOString().split('T')[0],
        stress_level: 4,
        sleep_hours: 5.2,
        physical_symptoms: ["Mất ngủ", "Lo âu đánh giá"],
        note: "Tuần sau có bài kiểm tra thao tác máy 5S của Line Leader, lo lắng không vượt qua kỳ thực tập.",
        ai_sentiment: "negative",
        risk_level: "warning",
        intervention_recommended: "Kết nối với Mentor cựu sinh viên cùng trường để được hướng dẫn mẹo thi 5S."
      }
    ];

    const mockArticles = [
      {
        id: "art-1",
        title: "Quy tắc 5S và An toàn lao động tại nhà máy LG Display",
        summary: "Hướng dẫn thực hành 5S và bảo hộ lao động ESD trong ca làm việc nhà máy.",
        content: "Quy tắc 5S bao gồm: Sàng lọc (Seiri), Sắp xếp (Seiton), Sạch sẽ (Seiso), Săn sóc (Seiketsu), Sẵn sàng (Shitsuke). Tuân thủ nghiêm ngặt đồ bảo hộ chống tĩnh điện và báo ngay cho Line Leader khi máy gặp sự cố.",
        category: "career",
        author_name: "Ban Cố vấn Thực tập",
        status: "published",
        helpful_count: 38,
        view_count: 142,
        tags: ["5s", "an-toan", "lg-display"],
        created_at: "2026-09-01T08:00:00Z"
      },
      {
        id: "art-2",
        title: "Bí quyết cân bằng nhịp sinh học và giấc ngủ khi đổi ca đêm",
        summary: "Kinh nghiệm ngủ sâu sau ca đêm và giảm thiểu kiệt sức nhịp sinh học.",
        content: "Khi tan ca sáng 8h trở về phòng, hãy đeo kính râm tránh ánh nắng mặt trời làm giảm tiết Melatonin. Dùng rèm cản sáng 100%, nhiệt độ phòng 22-24 độ C và ngâm chân nước ấm 15 phút.",
        category: "sleep",
        author_name: "Ban Cố vấn Tâm lý",
        status: "published",
        helpful_count: 45,
        view_count: 210,
        tags: ["giac-ngu", "ca-dem", "phuc-hoi"],
        created_at: "2026-09-03T10:00:00Z"
      },
      {
        id: "art-3",
        title: "Kỹ thuật Hít thở Box Breathing 4-4-4-4 hạ căng thẳng tức thì",
        summary: "Phương pháp hạ nhịp tim và ổn định tâm trí trong 3 phút khi bị quá tải áp lực.",
        content: "Hít vào 4 giây -> Nín thở 4 giây -> Thở ra nhẹ nhàng 4 giây -> Giữ nín thở 4 giây. Thực hiện 4 chu kỳ giúp kích hoạt hệ thần kinh đối giao cảm, lập tức lấy lại bình tĩnh.",
        category: "mental",
        author_name: "ThS. Tâm lý học Ứng dụng",
        status: "published",
        helpful_count: 52,
        view_count: 280,
        tags: ["hit-tho", "box-breathing", "giam-stress"],
        created_at: "2026-09-05T09:00:00Z"
      },
      {
        id: "art-4",
        title: "Mẹo giảm đau chân khi mang giày bảo hộ ESD đứng ca 12 tiếng",
        summary: "Bí kíp từ các anh chị khóa trước: lót giày silicon y tế và nâng cao chân khi ngủ.",
        content: "Mua sẵn 2 đôi miếng lót giày silicon có đệm vòm bàn chân. Sau khi tan ca, dùng dầu xoa bóp vuốt ngược bắp chân và kê cao chân trên gối 20cm khi ngủ để máu hồi lưu về tim.",
        category: "physical",
        author_name: "CLB Cựu Thực tập sinh",
        status: "published",
        helpful_count: 67,
        view_count: 315,
        tags: ["giay-esd", "dau-chan", "the-chat"],
        created_at: "2026-09-08T14:00:00Z"
      },
      {
        id: "art-5",
        title: "Quy ước sinh hoạt phòng ký túc xá lệch ca làm việc",
        summary: "Thống nhất giờ giấc và nguyên tắc tôn trọng lẫn nhau khi người làm ca ngày, người làm ca đêm.",
        content: "Thỏa thuận rõ nguyên tắc đóng cửa nhẹ tay, dùng tai nghe, không bật đèn trần phòng ngủ khi có bạn đang ngủ bù ca đêm. Chuẩn bị sẵn bịt tai chống ồn và bịt mắt 3D.",
        category: "social",
        author_name: "Ban Quản lý KTX",
        status: "published",
        helpful_count: 29,
        view_count: 175,
        tags: ["ktx", "phong-tro", "giao-tiep"],
        created_at: "2026-09-12T16:00:00Z"
      }
    ];

    const mockTasks = [
      {
        id: "tsk-1",
        title: "Tìm hiểu bản đồ nhà máy và nội quy phòng sạch ESD",
        description: "Ghi nhớ các cổng an ninh, vị trí tủ đồ locker, phòng thay đồ bảo hộ vô trùng và tuyến xe bus đưa đón.",
        phase: "preparation",
        pillar: "career",
        duration_minutes: 20,
        unlock_day: 1,
        is_active: true,
        completed_count: 118
      },
      {
        id: "tsk-2",
        title: "Chuẩn bị bộ vật dụng thích nghi giấc ngủ ca đêm",
        description: "Chuẩn bị rèm cản sáng, bịt tai chống ồn, kính râm và bình giữ nhiệt 1 lít.",
        phase: "preparation",
        pillar: "sleep",
        duration_minutes: 30,
        unlock_day: 2,
        is_active: true,
        completed_count: 95
      },
      {
        id: "tsk-3",
        title: "Làm quen với Line Leader và bạn cùng ca làm việc",
        description: "Chủ động chào hỏi, lưu số điện thoại khẩn cấp của Trưởng ca và Cố vấn trường.",
        phase: "adaptation",
        pillar: "social",
        duration_minutes: 15,
        unlock_day: 5,
        is_active: true,
        completed_count: 82
      },
      {
        id: "tsk-4",
        title: "Thực hành giãn cơ 3 phút sau giờ ăn trưa",
        description: "Thực hiện chuỗi bài tập xoay cổ tay, giãn cơ thắt lưng và bắp chân chống co rút.",
        phase: "adaptation",
        pillar: "physical",
        duration_minutes: 5,
        unlock_day: 7,
        is_active: true,
        completed_count: 76
      },
      {
        id: "tsk-5",
        title: "Tổng kết bài học kinh nghiệm tuần đầu vào sổ tay",
        description: "Viết ra 3 điều làm tốt và 2 lỗi sai thao tác cần cải thiện cho tuần tiếp theo.",
        phase: "sustain",
        pillar: "career",
        duration_minutes: 25,
        unlock_day: 14,
        is_active: true,
        completed_count: 54
      }
    ];

    const mockNotifications = [
      {
        id: "notif-1",
        title: "Nhắc nhở nạp năng lượng sau ca đêm",
        body: "Các bạn vừa hoàn thành ca đêm hãy uống một cốc nước ấm, ăn nhẹ và nghỉ ngơi trong phòng tối nhé!",
        type: "system",
        sent_at: "2026-10-13T07:30:00Z"
      },
      {
        id: "notif-2",
        title: "Cẩm nang mới: Giảm đau chân khi mang giày ESD",
        body: "Đã có bài viết hướng dẫn chi tiết cách chọn lót giày và massage chân từ cựu sinh viên trong mục Cẩm nang.",
        type: "new_article",
        sent_at: "2026-10-12T18:00:00Z"
      },
      {
        id: "notif-3",
        title: "Duy trì chuỗi Streak điểm danh tuần này",
        body: "Chúc mừng các bạn đã duy trì chuỗi 7 ngày liên tiếp! Hãy tiếp tục nhận Gacha quote mỗi sáng.",
        type: "streak_warning",
        sent_at: "2026-10-11T08:15:00Z"
      }
    ];

    return {
      stats: {
        total_users: 125,
        total_students: 120,
        today_checkins: 88,
        checkin_rate: 73.3,
        total_articles: mockArticles.length,
        total_tasks: mockTasks.length,
        total_completed_tasks: 425,
        burnout_risk_count: 3,
        low_sleep_count: 7,
        intern_phases: {
          preparation: 35,
          adaptation: 62,
          sustain: 23
        },
        pillar_averages: {
          sleep: 68.5,
          physical: 71.2,
          mental: 64.0,
          social: 76.4,
          career: 82.1
        }
      },
      students: mockStudents,
      alerts: mockAlerts,
      articles: mockArticles,
      tasks: mockTasks,
      notifications: mockNotifications
    };
  }

  // ─── API Fetcher with Auto-Fallback ───────────────────────────────────────────
  async function apiFetch(endpoint, options = {}) {
    if (STATE.isDemoMode) {
      return null;
    }

    const url = `${STATE.apiBaseUrl}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${STATE.adminToken}`,
      ...(options.headers || {})
    };

    try {
      const response = await fetch(url, { ...options, headers });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      return await response.json();
    } catch (err) {
      console.warn(`[API] Gọi thất bại tới ${endpoint}:`, err.message);
      return null;
    }
  }

  // ─── Initial Data Loader ──────────────────────────────────────────────────────
  async function loadAllData() {
    // 1. Thử kết nối API live
    const liveStats = await apiFetch('/admin/stats');
    
    if (liveStats) {
      // Backend đang chạy tốt!
      STATE.isDemoMode = false;
      DOM.statusIndicator.className = 'status-indicator live';
      const isRender = STATE.apiBaseUrl.includes('onrender.com');
      DOM.statusLabel.textContent = isRender ? 'Render Cloud (Live)' : `Live API (${new URL(STATE.apiBaseUrl).host})`;
      DOM.toggleDataModeBtn.textContent = 'Đổi sang Demo';
      STATE.stats = liveStats;

      // Fetch live collections
      const [students, alerts, articles, tasks, notifications] = await Promise.all([
        apiFetch('/admin/users'),
        apiFetch('/admin/burnout-alerts'),
        apiFetch('/admin/handbook'),
        apiFetch('/admin/tasks'),
        apiFetch('/admin/notifications/history')
      ]);

      STATE.students = students || [];
      STATE.alerts = alerts || [];
      STATE.articles = articles || [];
      STATE.tasks = tasks || [];
      STATE.notifications = notifications || [];
      showToast('Đã đồng bộ dữ liệu từ máy chủ Enigma Backend!', 'success');
    } else {
      // Tự động chuyển sang chế độ Demo Data phong phú
      STATE.isDemoMode = true;
      DOM.statusIndicator.className = 'status-indicator demo';
      DOM.statusLabel.textContent = 'Chế Độ Demo Data (Mượt mà)';
      DOM.toggleDataModeBtn.textContent = 'Thử Kết Nối Live';

      const mock = getMockData();
      STATE.stats = mock.stats;
      STATE.students = mock.students;
      STATE.alerts = mock.alerts;
      STATE.articles = mock.articles;
      STATE.tasks = mock.tasks;
      STATE.notifications = mock.notifications;
      showToast('Đang hiển thị chế độ Dữ liệu Demo trực quan!', 'info');
    }

    // Cập nhật UI
    updateBadges();
    renderKPIs();
    renderDashboardLists();
    renderDashboardCharts();
    renderStudentsTable();
    renderBurnoutCards();
    renderHandbookArticles();
    renderTasksTable();
    renderNotificationHistory();
  }

  // ─── Render Badges & KPIs ─────────────────────────────────────────────────────
  function updateBadges() {
    DOM.navBadgeStudents.textContent = STATE.students.length || '--';
    DOM.navBadgeAlerts.textContent = STATE.alerts.length || '0';
    DOM.navBadgeArticles.textContent = STATE.articles.length || '--';
    DOM.quickAlertCount.textContent = `${STATE.alerts.length} Ca Cảnh Báo`;
  }

  function renderKPIs() {
    const s = STATE.stats;
    if (!s) return;

    DOM.kpiTotalStudents.textContent = s.total_students || s.total_users || 0;
    DOM.kpiCheckinsToday.textContent = s.today_checkins || 0;
    DOM.kpiCheckinRate.textContent = `${s.checkin_rate || 0}% tỷ lệ`;
    DOM.kpiBurnoutRisk.textContent = s.burnout_risk_count || 0;
    DOM.kpiCompletedTasks.textContent = s.total_completed_tasks || 0;
  }

  // ─── Render Dashboard Feed & Watchlist ────────────────────────────────────────
  function renderDashboardLists() {
    // 1. Feed gần nhất
    const feedQuotes = [
      { user: "Nguyễn Minh Khang (B21DCCN045)", quote: "Vượt qua thử thách hôm nay sẽ là niềm tự hào của ngày mai.", time: "10 phút trước" },
      { user: "Trần Thị Thùy Linh (B21DCCN189)", quote: "Hít thở sâu 4 giây và thả lỏng bắp cơ vai gáy.", time: "25 phút trước" },
      { user: "Lê Hoàng Long (B21DCCN312)", quote: "An toàn lao động và 5S là nguyên tắc số một.", time: "42 phút trước" },
      { user: "Phạm Quốc Tuấn (B21DCCN408)", quote: "Uống đủ nước để duy trì sự tỉnh táo trong ca dài.", time: "1 giờ trước" }
    ];

    DOM.dashboardFeedList.innerHTML = feedQuotes.map(item => `
      <div class="feed-item">
        <div class="avatar">${item.user.charAt(0)}</div>
        <div class="feed-content">
          <div class="feed-user">
            <span>${item.user}</span>
            <span class="feed-time">${item.time}</span>
          </div>
          <p class="feed-quote">"${item.quote}"</p>
        </div>
      </div>
    `).join('');

    // 2. Watchlist kiệt sức
    if (STATE.alerts.length === 0) {
      DOM.dashboardWatchlist.innerHTML = `<p class="text-subtle text-center py-4">Hiện không có sinh viên nào trong vùng nguy cơ cao.</p>`;
    } else {
      DOM.dashboardWatchlist.innerHTML = STATE.alerts.slice(0, 3).map(a => `
        <div class="watchlist-item">
          <div class="watchlist-info">
            <h4>${a.full_name} (${a.student_id || 'Chưa có MSSV'})</h4>
            <p>${a.company_name} — Mức Stress: <strong class="text-danger">${a.stress_level}/5</strong> | Ngủ: ${a.sleep_hours}h</p>
          </div>
          <button class="btn btn-sm btn-danger-outline" onclick="window.EnigmaApp.openIntervention('${a.user_id}')">Can Thiệp</button>
        </div>
      `).join('');
    }
  }

  // ─── Render Charts with Chart.js ──────────────────────────────────────────────
  function renderDashboardCharts() {
    const s = STATE.stats || {
      pillar_averages: { sleep: 68, physical: 72, mental: 62, social: 76, career: 82 }
    };

    // 1. Radar Chart: 5 Trụ Cột Sức Khỏe
    const ctxPillars = document.getElementById('chart-pillars');
    if (ctxPillars) {
      if (STATE.charts.pillars) STATE.charts.pillars.destroy();

      STATE.charts.pillars = new Chart(ctxPillars, {
        type: 'radar',
        data: {
          labels: ['Giấc Ngủ (Sleep)', 'Thể Chất (Physical)', 'Tâm Lý (Mental)', 'Xã Hội (Social)', 'Sự Nghiệp (Career)'],
          datasets: [{
            label: 'Điểm Trung Bình Khóa Sinh Viên',
            data: [
              s.pillar_averages.sleep,
              s.pillar_averages.physical,
              s.pillar_averages.mental,
              s.pillar_averages.social,
              s.pillar_averages.career
            ],
            backgroundColor: 'rgba(99, 102, 241, 0.25)',
            borderColor: '#6366f1',
            borderWidth: 2,
            pointBackgroundColor: '#06b6d4',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#06b6d4',
            pointRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              min: 0,
              max: 100,
              ticks: { stepSize: 20, color: '#64748b', backdropColor: 'transparent' },
              grid: { color: 'rgba(51, 65, 85, 0.4)' },
              angleLines: { color: 'rgba(51, 65, 85, 0.5)' },
              pointLabels: {
                color: '#cbd5e1',
                font: { size: 11, family: 'Plus Jakarta Sans', weight: '600' }
              }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }

    // 2. Bar Chart: Phân bổ mức độ Stress
    const ctxStress = document.getElementById('chart-stress');
    if (ctxStress) {
      if (STATE.charts.stress) STATE.charts.stress.destroy();

      STATE.charts.stress = new Chart(ctxStress, {
        type: 'bar',
        data: {
          labels: ['1: Bình thản', '2: Nhẹ nhàng', '3: Trung bình', '4: Căng thẳng', '5: Rất căng thẳng'],
          datasets: [{
            label: 'Số lượng sinh viên',
            data: [28, 45, 32, 12, 3],
            backgroundColor: [
              '#10b981',
              '#34d399',
              '#f59e0b',
              '#f97316',
              '#f43f5e'
            ],
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              grid: { display: false },
              ticks: { color: '#94a3b8', font: { size: 11 } }
            },
            y: {
              grid: { color: 'rgba(51, 65, 85, 0.3)' },
              ticks: { color: '#94a3b8', font: { size: 11 } }
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }

    // 3. Line Chart: Xu hướng 7 ngày
    const ctxTrend = document.getElementById('chart-trend');
    if (ctxTrend) {
      if (STATE.charts.trend) STATE.charts.trend.destroy();

      STATE.charts.trend = new Chart(ctxTrend, {
        type: 'line',
        data: {
          labels: ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật'],
          datasets: [
            {
              label: 'Số lượt điểm danh',
              data: [82, 85, 78, 92, 89, 70, 88],
              borderColor: '#06b6d4',
              backgroundColor: 'rgba(6, 182, 212, 0.1)',
              fill: true,
              tension: 0.35,
              yAxisID: 'y'
            },
            {
              label: 'Giờ ngủ TB (h)',
              data: [6.8, 6.9, 6.5, 7.1, 6.7, 7.4, 7.2],
              borderColor: '#10b981',
              backgroundColor: 'transparent',
              borderDash: [5, 5],
              tension: 0.35,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          scales: {
            x: {
              grid: { color: 'rgba(51, 65, 85, 0.2)' },
              ticks: { color: '#94a3b8' }
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              grid: { color: 'rgba(51, 65, 85, 0.3)' },
              ticks: { color: '#06b6d4' }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              grid: { drawOnChartArea: false },
              ticks: { color: '#10b981' },
              min: 4,
              max: 9
            }
          },
          plugins: {
            legend: { display: false }
          }
        }
      });
    }
  }

  // ─── Render Students Directory Table ──────────────────────────────────────────
  function renderStudentsTable() {
    const search = DOM.studentsSearchInput.value.toLowerCase().trim();
    const phase = DOM.studentsFilterPhase.value;
    const risk = DOM.studentsFilterRisk.value;

    let filtered = STATE.students.filter(s => {
      // Search
      const matchSearch = !search ||
        (s.full_name && s.full_name.toLowerCase().includes(search)) ||
        (s.student_id && s.student_id.toLowerCase().includes(search)) ||
        (s.email && s.email.toLowerCase().includes(search)) ||
        (s.university && s.university.toLowerCase().includes(search));

      // Phase
      const matchPhase = !phase || s.current_phase === phase;

      // Risk
      let matchRisk = true;
      if (risk === 'high') matchRisk = s.is_high_risk;
      if (risk === 'active') matchRisk = s.is_active;

      return matchSearch && matchPhase && matchRisk;
    });

    if (filtered.length === 0) {
      DOM.studentsTbody.innerHTML = `
        <tr>
          <td colspan="9" class="text-center py-6 text-subtle">
            Không tìm thấy sinh viên nào phù hợp với bộ lọc tìm kiếm.
          </td>
        </tr>
      `;
      return;
    }

    const phaseNames = {
      preparation: '<span class="badge badge-primary">1. Chuẩn Bị</span>',
      adaptation: '<span class="badge badge-info">2. Hòa Nhập</span>',
      sustain: '<span class="badge badge-emerald">3. Duy Trì</span>'
    };

    DOM.studentsTbody.innerHTML = filtered.map(s => {
      const stressLvl = s.latest_stress_level || 2;
      return `
        <tr>
          <td>
            <div class="user-cell">
              <div class="avatar">${s.full_name ? s.full_name.charAt(0) : 'U'}</div>
              <div>
                <h4>${s.full_name}</h4>
                <p>${s.email}</p>
              </div>
            </div>
          </td>
          <td>
            <strong>${s.student_id || 'Chưa cập nhật'}</strong>
            <p class="text-muted">${s.university || 'N/A'}</p>
          </td>
          <td>
            <span>${s.company_name || 'LG Display'}</span>
            <p class="text-muted">${s.department || 'Ban sản xuất'}</p>
          </td>
          <td>${phaseNames[s.current_phase] || s.current_phase}</td>
          <td>
            <span class="stress-pill level-${stressLvl}">Mức ${stressLvl}/5</span>
          </td>
          <td><strong>${s.latest_sleep_hours || 7.0}h</strong></td>
          <td>🔥 ${s.current_streak || 0} ngày</td>
          <td>
            ${s.is_active 
              ? '<span class="badge badge-emerald">Hoạt động</span>' 
              : '<span class="badge badge-danger">Bị khóa</span>'}
          </td>
          <td class="text-right">
            <button class="btn btn-sm btn-secondary" onclick="window.EnigmaApp.openUserDetail('${s.id}')">Chi Tiết</button>
          </td>
        </tr>
      `;
    }).join('');
  }

  // ─── Render Burnout Alert Cards ───────────────────────────────────────────────
  function renderBurnoutCards() {
    if (STATE.alerts.length === 0) {
      DOM.burnoutCardsContainer.innerHTML = `
        <div class="card p-6 text-center text-subtle" style="grid-column: 1 / -1;">
          🎉 Tuyệt vời! Hiện tại không có sinh viên nào rơi vào ngưỡng cảnh báo kiệt sức trầm trọng.
        </div>
      `;
      return;
    }

    DOM.burnoutCardsContainer.innerHTML = STATE.alerts.map(a => `
      <div class="burnout-card ${a.risk_level}">
        <div class="burnout-card-header">
          <div>
            <h3 class="burnout-student-name">${a.full_name}</h3>
            <p class="text-subtle">${a.student_id || 'Chưa có MSSV'} — ${a.department}</p>
          </div>
          <span class="badge ${a.risk_level === 'critical' ? 'badge-danger pulse-dot' : 'badge-amber'}">
            ${a.risk_level === 'critical' ? 'RỦI RO ĐỎ' : 'CẢNH BÁO'}
          </span>
        </div>

        <div class="burnout-metrics-row">
          <div class="metric-badge-box">
            <span class="label">Mức Stress</span>
            <span class="val text-danger">${a.stress_level}/5</span>
          </div>
          <div class="metric-badge-box">
            <span class="label">Giờ Ngủ</span>
            <span class="val text-danger">${a.sleep_hours}h</span>
          </div>
          <div class="metric-badge-box">
            <span class="label">AI Sentiment</span>
            <span class="val">${a.ai_sentiment}</span>
          </div>
        </div>

        <div class="symptoms-tags">
          ${(a.physical_symptoms || []).map(sym => `<span class="symptom-tag">⚠️ ${sym}</span>`).join('')}
        </div>

        <div class="burnout-note-quote">
          "${a.note || 'Không có ghi chú thêm.'}"
        </div>

        <div class="card-footer-actions mt-auto">
          <button class="btn btn-sm btn-primary btn-block" onclick="window.EnigmaApp.openIntervention('${a.user_id}')">
            📞 Gửi Can Thiệp Tâm Lý & Lời Khuyên
          </button>
        </div>
      </div>
    `).join('');
  }

  // ─── Render Handbook Articles ─────────────────────────────────────────────────
  function renderHandbookArticles() {
    const search = DOM.handbookSearchInput.value.toLowerCase().trim();
    const cat = DOM.handbookFilterCategory.value;
    const stat = DOM.handbookFilterStatus.value;

    let filtered = STATE.articles.filter(art => {
      const matchSearch = !search ||
        (art.title && art.title.toLowerCase().includes(search)) ||
        (art.summary && art.summary.toLowerCase().includes(search)) ||
        (art.content && art.content.toLowerCase().includes(search));

      const matchCat = cat === 'all' || !cat || art.category === cat;
      const matchStat = !stat || art.status === stat;

      return matchSearch && matchCat && matchStat;
    });

    if (filtered.length === 0) {
      DOM.handbookArticlesContainer.innerHTML = `
        <div class="card p-6 text-center text-subtle" style="grid-column: 1 / -1;">
          Không tìm thấy bài viết cẩm nang nào. Nhấn "Thêm Bài Mới" để tạo bài viết đầu tiên!
        </div>
      `;
      return;
    }

    const catLabels = {
      sleep: '🌙 1. Giấc Ngủ',
      physical: '💪 2. Thể Chất',
      mental: '🧘 3. Tâm Lý',
      social: '🤝 4. Xã Hội',
      career: '🚀 5. Sự Nghiệp'
    };

    DOM.handbookArticlesContainer.innerHTML = filtered.map(art => `
      <div class="article-card">
        <span class="article-category-badge">${catLabels[art.category] || art.category}</span>
        <h3 class="article-card-title">${art.title}</h3>
        <p class="article-card-summary">${art.summary || art.content.slice(0, 120) + '...'}</p>
        
        <div class="article-meta-row">
          <span>Tác giả: <strong>${art.author_name || 'Cố vấn'}</strong></span>
          <div class="article-actions">
            <button class="btn btn-sm btn-secondary" onclick="window.EnigmaApp.editArticle('${art.id}')">Sửa</button>
            <button class="btn btn-sm btn-danger-outline" onclick="window.EnigmaApp.deleteArticle('${art.id}')">Xóa</button>
          </div>
        </div>
      </div>
    `).join('');
  }

  // ─── Render Tasks Table ───────────────────────────────────────────────────────
  function renderTasksTable() {
    const currentPhase = STATE.activeTaskPhase;
    const filtered = STATE.tasks.filter(t => t.phase === currentPhase);

    if (filtered.length === 0) {
      DOM.tasksTbody.innerHTML = `
        <tr>
          <td colspan="7" class="text-center py-6 text-subtle">
            Chưa có nhiệm vụ nào cho giai đoạn này.
          </td>
        </tr>
      `;
      return;
    }

    const pillarIcons = {
      sleep: '🌙 Giấc ngủ',
      physical: '💪 Thể chất',
      mental: '🧘 Tâm lý',
      social: '🤝 Xã hội',
      career: '🚀 Sự nghiệp'
    };

    DOM.tasksTbody.innerHTML = filtered.map(t => `
      <tr>
        <td>
          <strong>${t.title}</strong>
          <p class="text-muted">${t.description}</p>
        </td>
        <td><span class="badge badge-info">${pillarIcons[t.pillar] || t.pillar}</span></td>
        <td>⏱️ ${t.duration_minutes || 15} phút</td>
        <td>📅 Ngày thứ ${t.unlock_day || 1}</td>
        <td>✅ ${t.completed_count || 0} lượt</td>
        <td>
          ${t.is_active 
            ? '<span class="badge badge-emerald">Hoạt động</span>' 
            : '<span class="badge badge-subtle">Ẩn</span>'}
        </td>
        <td class="text-right">
          <button class="btn btn-sm btn-secondary" onclick="window.EnigmaApp.editTask('${t.id}')">Sửa</button>
        </td>
      </tr>
    `).join('');
  }

  // ─── Render Notification History ──────────────────────────────────────────────
  function renderNotificationHistory() {
    if (STATE.notifications.length === 0) {
      DOM.notificationHistoryList.innerHTML = `<p class="text-subtle text-center py-4">Chưa có thông báo nào được phát.</p>`;
      return;
    }

    DOM.notificationHistoryList.innerHTML = STATE.notifications.map(n => `
      <div class="history-item">
        <h4>📢 ${n.title}</h4>
        <p>${n.body}</p>
        <div class="history-meta">
          <span>Loại: <strong>${n.type}</strong></span>
          <span>${new Date(n.sent_at || Date.now()).toLocaleTimeString()} - ${new Date(n.sent_at || Date.now()).toLocaleDateString()}</span>
        </div>
      </div>
    `).join('');
  }

  // ─── User Detail Modal Handler ────────────────────────────────────────────────
  async function openUserDetail(userId) {
    let user = STATE.students.find(s => s.id === userId);
    if (!user) return;

    // Lấy thêm chi tiết từ API nếu có
    const detail = await apiFetch(`/admin/users/${userId}`);
    if (detail && detail.user) {
      user = { ...user, ...detail.user, ...detail.profile };
    }

    document.getElementById('um-fullname').textContent = user.full_name;
    document.getElementById('um-student-id').textContent = user.student_id || 'MSSV N/A';
    document.getElementById('um-phase').textContent = `Giai đoạn: ${user.current_phase || 'adaptation'}`;
    document.getElementById('um-avatar').textContent = user.full_name ? user.full_name.charAt(0) : 'U';
    document.getElementById('um-name-card').textContent = user.full_name;
    document.getElementById('um-email').textContent = user.email;
    document.getElementById('um-company').textContent = `${user.company_name || 'LG Display'} — ${user.department || 'Ban sản xuất'}`;

    // 5 Pillars scores
    const scores = user.initial_scores || { sleep: 70, physical: 65, mental: 60, social: 75, career: 80 };
    document.getElementById('um-pillar-scores').innerHTML = `
      <div class="pillar-score-row"><span>🌙 Giấc ngủ (Sleep):</span><strong>${scores.sleep}/100</strong></div>
      <div class="pillar-score-row"><span>💪 Thể chất (Physical):</span><strong>${scores.physical}/100</strong></div>
      <div class="pillar-score-row"><span>🧘 Tâm lý (Mental):</span><strong>${scores.mental}/100</strong></div>
      <div class="pillar-score-row"><span>🤝 Xã hội (Social):</span><strong>${scores.social}/100</strong></div>
      <div class="pillar-score-row"><span>🚀 Sự nghiệp (Career):</span><strong>${scores.career}/100</strong></div>
    `;

    // Nhật ký 7 ngày mẫu
    const sampleJournals = [
      { date: 'Hôm nay', stress: user.latest_stress_level || 2, sleep: user.latest_sleep_hours || 7.5, note: 'Hoàn thành ca tốt, không gặp trục trặc máy móc.' },
      { date: 'Hôm qua', stress: 3, sleep: 6.5, note: 'Hơi mỏi chân do đi lại nhiều giữa 2 line máy.' },
      { date: '2 ngày trước', stress: 2, sleep: 7.0, note: 'Đã quen với giờ ăn trưa tại nhà ăn công ty.' }
    ];

    document.getElementById('um-journals-list').innerHTML = sampleJournals.map(j => `
      <div class="ujournal-item">
        <div class="flex justify-between text-xs text-muted mb-1">
          <span>${j.date}</span>
          <span>Stress: <strong>${j.stress}/5</strong> | Ngủ: <strong>${j.sleep}h</strong></span>
        </div>
        <p class="text-xs">"${j.note}"</p>
      </div>
    `).join('');

    // Toggle status button
    const btnToggle = document.getElementById('um-btn-toggle-status');
    btnToggle.textContent = user.is_active ? 'Khóa Tài Khoản' : 'Mở Khóa Tài Khoản';
    btnToggle.onclick = async () => {
      const newStatus = !user.is_active;
      await apiFetch(`/admin/users/${user.id}/status`, {
        method: 'PUT',
        body: JSON.stringify({ is_active: newStatus })
      });
      user.is_active = newStatus;
      showToast(`Đã ${newStatus ? 'mở khóa' : 'khóa'} tài khoản ${user.full_name}`, 'success');
      renderStudentsTable();
      DOM.userModal.classList.remove('open');
    };

    DOM.userModal.classList.add('open');
  }

  // ─── Modal Close Listeners ────────────────────────────────────────────────────
  document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modalId = btn.getAttribute('data-close-modal');
      const targetModal = document.getElementById(modalId);
      if (targetModal) targetModal.classList.remove('open');
    });
  });

  // ─── Broadcast Notification Form ──────────────────────────────────────────────
  DOM.broadcastForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('notif-title').value.trim();
    const body = document.getElementById('notif-body').value.trim();
    const type = document.getElementById('notif-type').value;
    const target = document.getElementById('notif-target').value;

    const payload = { title, body, type, target_role: target };

    await apiFetch('/admin/notifications/broadcast', {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    // Add to local state
    STATE.notifications.unshift({
      id: `notif-${Date.now()}`,
      title,
      body,
      type,
      sent_at: new Date().toISOString()
    });

    showToast(`Đã phát thông báo thành công tới sinh viên!`, 'success');
    DOM.broadcastForm.reset();
    renderNotificationHistory();
  });

  // ─── Handbook Form & Modals ───────────────────────────────────────────────────
  DOM.btnCreateArticle.addEventListener('click', () => {
    document.getElementById('art-id').value = '';
    document.getElementById('art-title').value = '';
    document.getElementById('art-summary').value = '';
    document.getElementById('art-content').value = '';
    document.getElementById('art-tags').value = '';
    document.getElementById('article-modal-title').textContent = 'Thêm Bài Viết Cẩm Nang Mới & Đồng Bộ AI';
    DOM.articleModal.classList.add('open');
  });

  DOM.articleForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const artId = document.getElementById('art-id').value;
    const title = document.getElementById('art-title').value.trim();
    const category = document.getElementById('art-category').value;
    const status = document.getElementById('art-status').value;
    const summary = document.getElementById('art-summary').value.trim();
    const content = document.getElementById('art-content').value.trim();
    const tags = document.getElementById('art-tags').value.split(',').map(t => t.trim()).filter(Boolean);

    const payload = { title, category, status, summary, content, tags };

    if (artId) {
      // Update
      await apiFetch(`/admin/handbook/${artId}`, { method: 'PUT', body: JSON.stringify(payload) });
      const idx = STATE.articles.findIndex(a => a.id === artId);
      if (idx !== -1) {
        STATE.articles[idx] = { ...STATE.articles[idx], ...payload };
      }
      showToast('Đã cập nhật bài viết cẩm nang!', 'success');
    } else {
      // Create
      const res = await apiFetch('/admin/handbook', { method: 'POST', body: JSON.stringify(payload) });
      const newArt = {
        id: (res && res.id) || `art-${Date.now()}`,
        author_name: 'Quản Trị Viên',
        helpful_count: 0,
        view_count: 1,
        ...payload
      };
      STATE.articles.unshift(newArt);
      showToast('Đã xuất bản bài viết và đồng bộ vào ChromaDB RAG!', 'success');
    }

    DOM.articleModal.classList.remove('open');
    renderHandbookArticles();
    updateBadges();
  });

  // ─── Export Functions ─────────────────────────────────────────────────────────
  DOM.btnExportStudents.addEventListener('click', () => {
    const csvRows = [
      ['MSSV', 'Ho Va Ten', 'Email', 'Truong', 'Cong Ty', 'Giai Doan', 'Stress', 'Gio Ngu', 'Streak', 'Trang Thai'].join(',')
    ];

    STATE.students.forEach(s => {
      csvRows.push([
        s.student_id || '',
        `"${s.full_name || ''}"`,
        s.email || '',
        `"${s.university || ''}"`,
        `"${s.company_name || ''}"`,
        s.current_phase || '',
        s.latest_stress_level || 2,
        s.latest_sleep_hours || 7,
        s.current_streak || 0,
        s.is_active ? 'Active' : 'Locked'
      ].join(','));
    });

    const blob = new Blob([csvRows.join('\n')], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Enigma_Danh_Sach_Sinh_Vien_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    showToast('Đã xuất file CSV danh sách sinh viên!', 'success');
  });

  DOM.btnExportJson.addEventListener('click', () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(STATE, null, 2));
    const dlAnchorElem = document.createElement('a');
    dlAnchorElem.setAttribute("href", dataStr);
    dlAnchorElem.setAttribute("download", `Enigma_Export_${new Date().toISOString().split('T')[0]}.json`);
    dlAnchorElem.click();
    showToast('Đã xuất dữ liệu toàn hệ thống sang định dạng JSON!', 'success');
  });

  // ─── Settings Handlers ────────────────────────────────────────────────────────
  DOM.btnSaveSettings.addEventListener('click', () => {
    const newUrl = DOM.settingApiUrl.value.trim();
    const newToken = DOM.settingAdminToken.value.trim();
    STATE.apiBaseUrl = newUrl;
    STATE.adminToken = newToken;
    localStorage.setItem('enigma_api_url', newUrl);
    localStorage.setItem('enigma_admin_token', newToken);
    showToast('Đã lưu cấu hình kết nối API!', 'success');
    loadAllData();
  });

  DOM.btnTestConnection.addEventListener('click', async () => {
    showToast('Đang kiểm tra kết nối tới Backend...', 'info');
    const res = await apiFetch('/admin/stats');
    if (res) {
      showToast('Kết nối thành công tới FastAPI Server!', 'success');
    } else {
      showToast('Không thể kết nối. Kiểm tra xem FastAPI đã chạy trên cổng này chưa.', 'error');
    }
  });

  DOM.btnClearCache.addEventListener('click', () => {
    localStorage.clear();
    showToast('Đã xóa bộ nhớ đệm. Đang tải lại...', 'info');
    setTimeout(() => location.reload(), 1000);
  });

  // ─── Quick Event Listeners ────────────────────────────────────────────────────
  DOM.navItems.forEach(item => {
    item.addEventListener('click', () => switchTab(item.dataset.tab));
  });

  DOM.btnRefresh.addEventListener('click', () => {
    showToast('Đang làm mới dữ liệu...', 'info');
    loadAllData();
  });

  DOM.btnQuickBroadcast.addEventListener('click', () => {
    switchTab('notifications');
  });

  DOM.toggleDataModeBtn.addEventListener('click', () => {
    STATE.isDemoMode = !STATE.isDemoMode;
    loadAllData();
  });

  DOM.mobileMenuBtn.addEventListener('click', () => {
    DOM.sidebar.classList.toggle('mobile-open');
  });

  DOM.taskPhaseSwitcher.querySelectorAll('button').forEach(btn => {
    btn.addEventListener('click', () => {
      DOM.taskPhaseSwitcher.querySelectorAll('button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      STATE.activeTaskPhase = btn.dataset.phase;
      renderTasksTable();
    });
  });

  DOM.studentsSearchInput.addEventListener('input', renderStudentsTable);
  DOM.studentsFilterPhase.addEventListener('change', renderStudentsTable);
  DOM.studentsFilterRisk.addEventListener('change', renderStudentsTable);

  DOM.handbookSearchInput.addEventListener('input', renderHandbookArticles);
  DOM.handbookFilterCategory.addEventListener('change', renderHandbookArticles);
  DOM.handbookFilterStatus.addEventListener('change', renderHandbookArticles);

  // ─── Public Window API for inline onclick handlers ───────────────────────────
  window.EnigmaApp = {
    openUserDetail,
    openIntervention: (userId) => {
      const user = STATE.students.find(s => s.id === userId);
      const name = user ? user.full_name : 'sinh viên';
      const advice = prompt(`Gửi tin nhắn can thiệp khẩn tới ${name}:`, `Chào bạn, Cố vấn thực tập đã nhận được thông tin ghi chú tâm trạng của bạn. Hãy liên hệ với Cố vấn qua số 0988.xxx.xxx hoặc phòng y tế nhé!`);
      if (advice) {
        showToast(`Đã gửi tin nhắn can thiệp tâm lý tới ${name}!`, 'success');
      }
    },
    editArticle: (artId) => {
      const art = STATE.articles.find(a => a.id === artId);
      if (!art) return;
      document.getElementById('art-id').value = art.id;
      document.getElementById('art-title').value = art.title;
      document.getElementById('art-category').value = art.category;
      document.getElementById('art-status').value = art.status;
      document.getElementById('art-summary').value = art.summary || '';
      document.getElementById('art-content').value = art.content || '';
      document.getElementById('art-tags').value = (art.tags || []).join(', ');
      document.getElementById('article-modal-title').textContent = 'Chỉnh Sửa Bài Viết Cẩm Nang';
      DOM.articleModal.classList.add('open');
    },
    deleteArticle: async (artId) => {
      if (confirm('Bạn có chắc muốn xóa bài viết cẩm nang này không?')) {
        await apiFetch(`/admin/handbook/${artId}`, { method: 'DELETE' });
        STATE.articles = STATE.articles.filter(a => a.id !== artId);
        showToast('Đã xóa bài viết cẩm nang!', 'success');
        renderHandbookArticles();
        updateBadges();
      }
    },
    editTask: (taskId) => {
      const task = STATE.tasks.find(t => t.id === taskId);
      if (!task) return;
      document.getElementById('task-id').value = task.id;
      document.getElementById('task-title').value = task.title;
      document.getElementById('task-phase').value = task.phase;
      document.getElementById('task-pillar').value = task.pillar;
      document.getElementById('task-duration').value = task.duration_minutes || 15;
      document.getElementById('task-unlock-day').value = task.unlock_day || 1;
      document.getElementById('task-desc').value = task.description || '';
      document.getElementById('task-modal-title').textContent = 'Chỉnh Sửa Nhiệm Vụ Thích Nghi';
      DOM.taskModal.classList.add('open');
    }
  };

  // ─── Initialize App on Page Load ──────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    loadAllData();
  });

})();
