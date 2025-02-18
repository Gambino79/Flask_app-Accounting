document.addEventListener("DOMContentLoaded", (event) => {
    const dateInput = document.querySelector("#date_received");
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based
    const day = String(today.getDate()).padStart(2, "0");
    const formattedDate = `${year}-${month}-${day}`;
    dateInput.value = formattedDate;
  });

  document.addEventListener("DOMContentLoaded", (event) => {
    const dateInput = document.querySelector("#date_paid");
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based
    const day = String(today.getDate()).padStart(2, "0");
    const formattedDate = `${year}-${month}-${day}`;
    dateInput.value = formattedDate;
  });

  document.addEventListener("DOMContentLoaded", (event) => {
    const dateInput = document.querySelector("#date_month_ex");
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based
    const day = String(today.getDate()).padStart(2, "0");
    const formattedDate = `${year}-${month}-${day}`;
    dateInput.value = formattedDate;
  });

  document.addEventListener("DOMContentLoaded", (event) => {
    const dateInput = document.querySelector("#date_month_re");
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, "0"); // Months are zero-based
    const day = String(today.getDate()).padStart(2, "0");
    const formattedDate = `${year}-${month}-${day}`;
    dateInput.value = formattedDate;
  });