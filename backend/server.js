import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { login, register, logout, getDashboardData, updateDashboardData, getDashboardFilteredData } from "./api/auth.js";  // ← Add updateDashboardData
import { verifyToken } from "./middleware/auth.js";

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: "*",
  credentials: true
}));
app.use(express.json());

// Routes

// Auth Routes (Public)
app.post("/api/auth/register", register);
app.post("/api/auth/login", login);
app.post("/api/auth/logout", logout);

// Dashboard Routes (Protected)
app.get("/api/dashboard", verifyToken, getDashboardData);
app.put("/api/dashboard/:id", verifyToken, updateDashboardData);

// Protected Routes
app.get("/api/profile", verifyToken, (req, res) => {
  res.json({ message: "Protected route", user: req.user });
});

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "Backend is running" });
});

// 404 Handler
app.use((req, res) => {
  console.log('❌ Route not found:', req.method, req.path);
  res.status(404).json({ message: "Route not found", path: req.path });
});

// Error handling
app.use((err, req, res, next) => {
  console.error(err);
  res.status(500).json({ message: "Server error", error: err.message });
});

app.listen(PORT, () => {
  console.log(`🚀 Backend running on port ${PORT}`);
  console.log(`📍 API URL: http://localhost:${PORT}`);
});
