const API_BASE_URL = "http://127.0.0.1:5001/api";
const LOGIN_PAGE_URL = "/frontend/customer/login.html";

const token = localStorage.getItem("authToken");
const userRole = localStorage.getItem("userRole");

async function loadDashboardData() {
  if (!token) {
    alert("Bạn chưa đăng nhập. Đang chuyển hướng...");
    window.location.replace(LOGIN_PAGE_URL);
    return;
  }

  try {
    const response = await fetch(API_BASE_URL + "/summary", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });

    if (!response.ok) {
      throw new Error("Phiên làm việc hết hạn hoặc không có quyền.");
    }

    const data = await response.json();
    document.getElementById("user-name").textContent =
      data.user_name || "Khách";
    document.getElementById("pending-orders").textContent =
      data.pending_orders || 0;
    document.getElementById("new-notifications").textContent =
      data.notifications || 0;
  } catch (error) {
    console.error("Lỗi tải dashboard:", error.message);
    alert("Phiên làm việc hết hạn. Vui lòng đăng nhập lại.");
    localStorage.removeItem("authToken");
    localStorage.removeItem("userRole");
    window.location.replace(LOGIN_PAGE_URL);
  }
}

document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.removeItem("authToken");
  localStorage.removeItem("userRole");
  alert("Đã đăng xuất thành công.");
  window.location.replace(LOGIN_PAGE_URL);
});

loadDashboardData();
