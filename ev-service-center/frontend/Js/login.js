const API_LOGIN_URL = "http://127.0.0.1:5001/api/login";

document.getElementById("login-form").addEventListener("submit", handleLogin);

// Hàm quyết định trang Dashboard dựa trên vai trò
function getDashboardUrl(role) {
  role = role ? role.toLowerCase() : "customer";
  if (role === "admin") {
    return "/frontend/admin/index.html";
  } else if (role === "staff" || role === "technician") {
    return "/frontend/staff/index.html";
  } else {
    return "/frontend/customer/index.html"; // ✅ Đường dẫn tuyệt đối
  }
}

async function handleLogin(event) {
  event.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorDisplay = document.getElementById("login-error");
  const submitButton = event.target.querySelector('button[type="submit"]');

  errorDisplay.style.display = "none";
  submitButton.disabled = true;
  submitButton.textContent = "Đang xử lý...";

  try {
    const response = await fetch(API_LOGIN_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    // --- Cải tiến: Kiểm tra phản hồi rỗng trước khi phân tích JSON ---
    const responseText = await response.text();
    let data = {};
    if (responseText) {
      try {
        data = JSON.parse(responseText);
      } catch (e) {
        console.error("Lỗi phân tích JSON từ server:", responseText);
        throw new Error("Phản hồi không phải JSON hợp lệ.");
      }
    }
    // --- End Cải tiến ---

    if (response.ok) {
      // Trường hợp 200 OK
      const { token, role } = data;

      if (!token || !role) {
        // Nếu 200 nhưng thiếu dữ liệu (token hoặc role)
        throw new Error("Phản hồi thành công nhưng thiếu token/vai trò.");
      }

      localStorage.setItem("authToken", token);
      localStorage.setItem("userRole", role);

      const redirectUrl = getDashboardUrl(role);
      window.location.replace(redirectUrl);
      return; // Ngăn chặn khối finally chạy ngay lập tức
    } else {
      // Trường hợp lỗi logic (401, 403,...)
      const errorMessage =
        data.message || "Tên đăng nhập hoặc mật khẩu không chính xác.";
      errorDisplay.textContent = errorMessage;
      errorDisplay.style.display = "block";
    }
  } catch (error) {
    // Lỗi kết nối mạng thực sự, lỗi token/role bị thiếu, hoặc lỗi JSON không hợp lệ
    console.error("Lỗi xử lý phản hồi:", error);
    errorDisplay.textContent = error.message.includes("token/vai trò")
      ? error.message
      : "Lỗi xử lý phản hồi từ máy chủ. Vui lòng thử lại.";
    errorDisplay.style.display = "block";
  } finally {
    // Luôn bật lại nút nếu không có chuyển hướng
    if (submitButton && submitButton.disabled) {
      submitButton.disabled = false;
      submitButton.textContent = "Đăng nhập";
    }
  }
}
