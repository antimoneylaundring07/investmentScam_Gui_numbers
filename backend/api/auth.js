import supabase from "../db/supabase.js";
import bcrypt from "bcryptjs";
import { generateToken } from "../middleware/auth.js";

// Register new user
export const register = async (req, res) => {
  try {
    const { email, password, name } = req.body;

    if (!email || !password || !name) {
      return res.status(400).json({ message: "Email, password, and name required" });
    }

    // Check if user exists
    const { data: existingUser } = await supabase
      .from("users")
      .select("email")
      .eq("email", email)
      .single();

    if (existingUser) {
      return res.status(409).json({ message: "User already exists" });
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Insert user
    const { data, error } = await supabase
      .from("users")
      .insert([{ email, password: hashedPassword, name }])
      .select()
      .single();

    if (error) throw error;

    const token = generateToken({ id: data.id, email: data.email, role: data.role });
    res.status(201).json({ message: "User registered", user: data, token });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

// Login user
export const login = async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ message: "Username and password required" });
    }

    // Get user by username
    const { data: user, error } = await supabase
      .from("users")
      .select("*")
      .eq("username", username)
      .single();

    if (error || !user) {
      return res.status(401).json({ message: "Invalid username or password" });
    }

    // Check password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({ message: "Invalid username or password" });
    }

    const token = generateToken({ id: user.id, username: user.username, role: user.role });
    res.json({ message: "Login successful", user: { id: user.id, username: user.username, name: user.name, role: user.role }, token });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};


// Logout (frontend handles token removal)
export const logout = (req, res) => {
  res.json({ message: "Logout successful" });
};
