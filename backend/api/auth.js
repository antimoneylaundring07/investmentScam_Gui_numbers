import supabase from "../db/supabase.js";
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
      .from("login")
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
      .from("login")
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

// Login user (ONLY username + password, NO hashing)
export const login = async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return res.status(400).json({ message: "Username and password required" });
    }

    // Fetch user
    const { data: user, error } = await supabase
      .from("login")
      .select("*")
      .eq("username", username)
      .maybeSingle();

    if (error) {
      console.error("Supabase query error:", error);
      return res.status(500).json({ message: "Database error" });
    }

    if (!user) {
      return res.status(401).json({ message: "Invalid username or password" });
    }

    // Compare plain passwords
    if (user.password !== password) {
      return res.status(401).json({ message: "Invalid username or password" });
    }

    const token = generateToken({ username: user.username });

    return res.json({
      message: "Login successful",
      user: { username: user.username },
      token,
    });
  } catch (error) {
    console.error("Login error:", error);
    return res.status(500).json({ message: error.message });
  }
};

// Logout (frontend handles token removal)
export const logout = (req, res) => {
  res.json({ message: "Logout successful" });
};
