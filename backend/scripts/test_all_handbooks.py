import sys
import asyncio
sys.path.insert(0, 'backend')

from app.core.handbook_data import HANDBOOK_ARTICLES
from app.services.vector_store_service import VectorStoreService, _collection
from app.services.advanced_rag_service import AdvancedRAGService

# Test queries: both natural questions and exact handbook titles as clicked from the UI
TEST_CASES = [
    {
        "id": "h1-food-trang-due",
        "title": "Mẹo ăn uống tiết kiệm và an toàn quanh KCN Tràng Duệ và An Dương",
        "queries": [
            "Mẹo ăn uống tiết kiệm & an toàn quanh KCN Tràng Duệ",
            "Quanh KCN Tràng Duệ có quán cơm nào rẻ và sạch không?",
        ]
    },
    {
        "id": "h2-ergonomics-back-neck",
        "title": "Xử lý đau mỏi vai gáy và thắt lưng do đứng chuyền liên tục",
        "queries": [
            "Xử lý đau mỏi vai gáy & thắt lưng do đứng chuyền liên tục",
            "Tôi đứng chuyền 12 tiếng bị đau cứng cổ và mỏi thắt lưng thì làm sao?",
        ]
    },
    {
        "id": "h3-esd-shoes-care",
        "title": "Bí quyết bảo vệ bàn chân khi mang giày bảo hộ ESD ca 12 tiếng",
        "queries": [
            "Bí quyết bảo vệ bàn chân khi mang giày bảo hộ ESD 12 tiếng",
            "Chân tôi rất đau và phồng rộp khi mang giày bảo hộ ESD",
        ]
    },
    {
        "id": "h4-rights-ot-allowance",
        "title": "Quy định làm thêm giờ OT, phụ cấp ca đêm và quyền lợi hợp đồng thực tập",
        "queries": [
            "Quyền lợi OT, phụ cấp ca đêm và quy chế làm thêm giờ",
            "Làm thêm giờ ban đêm thì được tính bao nhiêu phần trăm lương?",
        ]
    },
    {
        "id": "h5-sleep-night-shift",
        "title": "Bí quyết cân bằng nhịp sinh học và giấc ngủ sâu khi chuyển đổi ca đêm",
        "queries": [
            "Bí quyết cân bằng nhịp sinh học & giấc ngủ khi chuyển ca đêm",
            "Làm ca đêm về sáng không ngủ được, làm sao để ngủ ngon ban ngày?",
        ]
    },
    {
        "id": "h6-rent-room-security",
        "title": "Kinh nghiệm thuê phòng trọ an ninh và chi phí hợp lý gần khu công nghiệp",
        "queries": [
            "Kinh nghiệm thuê phòng trọ an ninh & chi phí hợp lý quanh nhà máy",
            "Tìm phòng trọ gần khu công nghiệp cần lưu ý những gì về giá điện nước?",
        ]
    },
    {
        "id": "h7-roommate-shift-rules",
        "title": "Quy tắc ứng xử và giải quyết mâu thuẫn phòng trọ khi lệch ca làm việc",
        "queries": [
            "Quy tắc ứng xử và giải quyết mâu thuẫn phòng trọ khi lệch ca",
            "Bạn cùng phòng làm ca ngày còn tôi làm ca đêm, ồn ào quá thì giải quyết sao?",
        ]
    },
    {
        "id": "h8-5s-cleanroom-safety",
        "title": "Quy tắc 5S và an toàn tĩnh điện ESD trong phòng sạch công nghiệp",
        "queries": [
            "Quy tắc 5S và An toàn tĩnh điện (ESD) trong phòng sạch công nghiệp",
            "Nội quy 5S và quy định chống tĩnh điện trong phòng sạch gồm những gì?",
        ]
    },
    {
        "id": "h9-box-breathing-stress",
        "title": "Kỹ thuật Hít thở Box Breathing 4-4-4-4 giảm căng thẳng và hoảng loạn tức thì",
        "queries": [
            "Kỹ thuật Hít thở Box Breathing 4-4-4-4 giảm căng thẳng tức thì",
            "Tôi cảm thấy hoảng loạn và thở gấp khi bị áp lực chuyền, có cách thở nào hạ nhịp tim không?",
        ]
    },
    {
        "id": "h10-leave-shift-swap",
        "title": "Quy trình xin nghỉ phép, đổi ca làm việc và xử lý khi bị ốm sốt đột xuất",
        "queries": [
            "Quy trình xin nghỉ phép, đổi ca làm việc và xử lý khi bị ốm sốt đột xuất",
            "Bị ốm sốt đột xuất buổi sáng thì làm thủ tục xin nghỉ phép với Leader như thế nào?",
        ]
    },
    {
        "id": "h11-bus-transportation",
        "title": "Kinh nghiệm sử dụng xe buýt đưa đón nhân viên và văn hóa đi xe an toàn",
        "queries": [
            "Kinh nghiệm sử dụng xe buýt đưa đón nhân viên và văn hóa đi xe an toàn",
            "Đi xe buýt công ty đưa đón cần chú ý những gì và đón ở đâu?",
        ]
    },
    {
        "id": "h12-emergency-stop-safety",
        "title": "Hướng dẫn xử lý sự cố an toàn, nút dừng khẩn cấp E-Stop và cảnh báo máy",
        "queries": [
            "Hướng dẫn xử lý sự cố an toàn, nút dừng khẩn cấp E-Stop và cảnh báo máy",
            "Khi máy móc phát ra tiếng lạ hoặc kẹt hàng thì có được thò tay vào sửa không?",
        ]
    },
    {
        "id": "h13-first-aid-exhaustion",
        "title": "Kinh nghiệm sơ cứu nhanh kiệt sức do nhiệt, tụt đường huyết và say nắng",
        "queries": [
            "Kinh nghiệm sơ cứu nhanh kiệt sức do nhiệt, tụt đường huyết và say nắng",
            "Đang đứng chuyền mà bị chóng mặt, vã mồ hôi lạnh sắp ngất thì xử lý sơ cứu ra sao?",
        ]
    },
    {
        "id": "h14-workplace-communication",
        "title": "Cách giao tiếp hiệu quả với Line Leader, Mentor và kỹ sư quản lý ca",
        "queries": [
            "Cách giao tiếp hiệu quả với Line Leader, Mentor và kỹ sư quản lý ca",
            "Báo cáo sự cố cho Trưởng ca như thế nào cho đúng tác phong công nghiệp?",
        ]
    },
    {
        "id": "h15-mindset-non-major",
        "title": "Tâm thế thích ứng khi làm việc trái ngành tại nhà máy sản xuất",
        "queries": [
            "Tâm thế thích ứng khi làm việc trái ngành tại nhà máy sản xuất",
            "Học công nghệ thông tin/kinh tế nhưng đi thực tập đứng máy sản xuất thấy nản lòng",
        ]
    },
    {
        "id": "h16-internship-report-guide",
        "title": "Hướng dẫn viết nhật ký thực tập và hoàn thành báo cáo tốt nghiệp đạt điểm cao",
        "queries": [
            "Hướng dẫn viết nhật ký thực tập và hoàn thành báo cáo tốt nghiệp đạt điểm cao",
            "Làm sao để viết báo cáo thực tập tốt nghiệp đầy đủ số liệu và xin mộc công ty?",
        ]
    },
    {
        "id": "h17-insurance-benefits",
        "title": "Chính sách bảo hiểm y tế, bảo hiểm tai nạn lao động cho thực tập sinh",
        "queries": [
            "Chính sách bảo hiểm y tế, bảo hiểm tai nạn lao động cho thực tập sinh",
            "Đi thực tập ở tỉnh khác thì thẻ bảo hiểm y tế sinh viên có khám chữa bệnh được không?",
        ]
    },
    {
        "id": "h18-financial-management",
        "title": "Kỹ năng quản lý tài chính và chi tiêu thông minh với tiền phụ cấp thực tập",
        "queries": [
            "Kỹ năng quản lý tài chính và chi tiêu thông minh với tiền phụ cấp thực tập",
            "Nhận được phụ cấp thực tập thì nên chia tiền ăn ở tiết kiệm như thế nào để không bị nợ nần?",
        ]
    },
    {
        "id": "h19-noise-pressure-adaptation",
        "title": "Mẹo thích nghi với tiếng ồn còi báo và môi trường áp lực cao trong xưởng",
        "queries": [
            "Mẹo thích nghi với tiếng ồn còi báo và môi trường áp lực cao trong xưởng",
            "Xưởng ồn ào và phải soi kính hiển vi liên tục làm mắt bị mờ và nhức đầu thì làm sao?",
        ]
    },
    {
        "id": "h20-phq4-mental-screening",
        "title": "Thang đo Y khoa PHQ-4: Sàng lọc nhanh trầm cảm và lo âu cho sinh viên ca kíp",
        "queries": [
            "Thang đo Y khoa PHQ-4: Sàng lọc nhanh trầm cảm & lo âu cho công nhân ca kíp (PMC8038412)",
            "Thang đo PHQ-4 là gì và điểm số bao nhiêu thì cần đi gặp chuyên gia tâm lý?",
        ]
    }
]

def run_tests():
    total_tests = 0
    passed_tests = 0
    results = []

    print(f"=== BAT DAU KIEM THU TOAN DIEN {len(TEST_CASES)} CHU DE CAM NANG ===")
    print(f"Tong so chunks trong ChromaDB hien tai: {_collection.count()}\n")

    for tc in TEST_CASES:
        expected_id = tc["id"]
        expected_title = tc["title"]
        print(f"--- [TESTING] {expected_id}: {expected_title[:50]}... ---")

        for q in tc["queries"]:
            total_tests += 1
            expanded = AdvancedRAGService.expand_query(q)
            
            # Hybrid search through expanded queries
            all_chunks = []
            seen = set()
            for exp_q in expanded:
                res = VectorStoreService.search_similar_chunks(exp_q, top_k=3)
                for r in res:
                    chunk_str = r.get("chunk", "")
                    if chunk_str and chunk_str not in seen:
                        seen.add(chunk_str)
                        all_chunks.append(r)

            all_chunks.sort(key=lambda x: x.get("similarity", 0.0), reverse=True)
            top_3 = [c for c in all_chunks if c.get("similarity", 0.0) >= 0.40][:3]

            # Verify if expected article is in top_3
            matched = any(c.get("metadata", {}).get("article_id") == expected_id for c in top_3)
            best_sim = 0.0
            best_title = "None"
            if top_3:
                best_sim = top_3[0].get("similarity", 0.0)
                best_title = top_3[0].get("metadata", {}).get("title", "")

            # Check if matching chunk specifically
            matching_sim = 0.0
            for c in top_3:
                if c.get("metadata", {}).get("article_id") == expected_id:
                    matching_sim = c.get("similarity", 0.0)
                    break

            if matched and matching_sim >= 0.40:
                passed_tests += 1
                status_str = f"[PASS] (Sim: {matching_sim:.4f} >= 0.40)"
            else:
                status_str = f"[FAIL] (Best: {best_title[:30]} | Sim: {best_sim:.4f})"

            print(f"  Q: '{q[:55]}...'")
            print(f"     -> {status_str}")

    print("\n" + "="*60)
    print(f"KET QUA KIEM THU: {passed_tests}/{total_tests} tests PASSED (Ty le: {passed_tests/total_tests*100:.1f}%)")
    print("="*60)

if __name__ == "__main__":
    run_tests()

