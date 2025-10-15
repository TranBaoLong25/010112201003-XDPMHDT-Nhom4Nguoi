const API_REGISTER_URL = "http://127.0.0.1:5001/api/register";
const LOGIN_PAGE_URL = "login.html";

document
  .getElementById("register-form")
  .addEventListener("submit", handleRegister);

async function handleRegister(event) {
  // Đổi tên hàm thành handleRegister để tránh lỗi
  event.preventDefault();

  const username = document.getElementById("username").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm-password").value;
  const messageDisplay = document.getElementById("register-message");
  const submitButton = event.target.querySelector('button[type="submit"]');

  // [1] Thiết lập lại trạng thái thông báo và nút
  messageDisplay.textContent = "";
  messageDisplay.classList.remove("error-message", "success-message");
  messageDisplay.style.display = "none";
  submitButton.disabled = true;
  submitButton.textContent = "Đang xử lý...";

  // [2] Kiểm tra Frontend
  if (password !== confirmPassword) {
    messageDisplay.textContent = "Lỗi: Mật khẩu xác nhận không khớp.";
    messageDisplay.classList.add("error-message");
    messageDisplay.style.display = "block";
    submitButton.disabled = false;
    submitButton.textContent = "Đăng ký";
    return;
  }
  if (password.length < 6) {
    messageDisplay.textContent = "Lỗi: Mật khẩu phải có ít nhất 6 ký tự.";
    messageDisplay.classList.add("error-message");
    messageDisplay.style.display = "block";
    submitButton.disabled = false;
    submitButton.textContent = "Đăng ký";
    return;
  }

  // [3] Gọi API Đăng ký
  try {
    const response = await fetch(API_REGISTER_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
        role: "customer",
      }),
    });

    const data = await response.json();

    if (response.ok) {
      messageDisplay.textContent =
        "Đăng ký thành công! Đang chuyển hướng đến trang Đăng nhập...";
      messageDisplay.classList.add("success-message");
      messageDisplay.style.display = "block";

      setTimeout(() => {
        window.location.href = LOGIN_PAGE_URL;
      }, 2000);
    } else {
      const errorMessage =
        data.message || "Lỗi đăng ký không xác định. Vui lòng thử lại.";
      messageDisplay.textContent = errorMessage;
      messageDisplay.classList.add("error-message");
      messageDisplay.style.display = "block";
    }
  } catch (error) {
    // Lỗi kết nối
    console.error("Lỗi kết nối hoặc xử lý:", error);
    messageDisplay.textContent =
      "Không thể kết nối đến máy chủ. (Kiểm tra cổng 5001 và CORS).";
    messageDisplay.classList.add("error-message");
    messageDisplay.style.display = "block";
  } finally {
    // [4] Luôn bật lại nút sau khi xử lý xong (trừ khi đã chuyển hướng)
    if (submitButton.disabled) {
      submitButton.disabled = false;
      submitButton.textContent = "Đăng ký";
    }
  }
}
