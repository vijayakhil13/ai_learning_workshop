async function checkBackend() {
  try {
    const response = await fetch("http://127.0.0.1:8000/health");
    const data = await response.json();
    console.log("Backend response:", data);
  } catch (error) {
    console.error("Failed to reach backend:", error);
  }
}