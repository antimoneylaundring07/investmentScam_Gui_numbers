import supabase from "../db/supabase.js";
import { generateToken } from "../middleware/auth.js";

// Simple login supporting two tables: 'login' (users) and 'admin' (admins).
export const login = async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ message: "Username and password required" });
    }

    // First, try regular users table
    const { data: user, error: userError } = await supabase
      .from("login")
      .select("*")
      .eq("username", username)
      .maybeSingle();

    if (userError) {
      console.error("Supabase user query error:", userError);
      return res.status(500).json({ message: "Database error" });
    }

    if (user && user.password === password) {
      const token = generateToken({ username: user.username, role: "user" });
      return res.json({
        message: "Login successful",
        user: { username: user.username, role: "user" },
        token,
      });
    }

    // If not found in users, try admin table
    const { data: admin, error: adminError } = await supabase
      .from("admin")
      .select("*")
      .eq("username", username)
      .maybeSingle();

    if (adminError) {
      console.error("Supabase admin query error:", adminError);
      return res.status(500).json({ message: "Database error" });
    }

    if (admin && admin.password === password) {
      const token = generateToken({ username: admin.username, role: "admin" });
      return res.json({
        message: "Login successful",
        user: { username: admin.username, role: "admin" },
        token,
      });
    }

    // No match
    return res.status(401).json({ message: "Invalid username or password" });
  } catch (error) {
    console.error("Login handler error:", error);
    return res.status(500).json({ message: error?.message || String(error) });
  }
};

// (Optional) simple register that inserts into 'login' table (keeps only username & password)
export const register = async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ message: "Username and password required" });
    }

    const { data: existingUser, error: existingError } = await supabase
      .from("login")
      .select("*")
      .eq("username", username)
      .maybeSingle();

    if (existingError) {
      console.error("Supabase exists query error:", existingError);
      return res.status(500).json({ message: "Database error" });
    }

    if (existingUser) {
      return res.status(409).json({ message: "User already exists" });
    }

    const { data, error } = await supabase
      .from("login")
      .insert([{ username, password }])
      .select();

    if (error) {
      console.error("Supabase insert error:", error);
      return res.status(500).json({ message: "Database error" });
    }

    return res.status(201).json({ message: "Registered successfully", user: data[0] });
  } catch (error) {
    console.error("Register handler error:", error);
    return res.status(500).json({ message: error?.message || String(error) });
  }
};

// Logout (frontend handles token removal)
export const logout = (req, res) => {
  res.json({ message: "Logout successful" });
};

export const getDashboardData = async (req, res) => {
  try {
    console.log("📊 Dashboard request received from:", req.user);
    const { data, error } = await supabase
      .from("numbers")  // Your table name
      .select("*")
      .order("id", { ascending: true });

    if (error) {
      console.error("Supabase dashboard query error:", error);
      return res.status(400).json({ message: error.message });
    }

    res.json({ data: data || [] });
  } catch (error) {
    console.error("Dashboard data error:", error);
    res.status(500).json({ message: error.message || "Server error" });
  }
};