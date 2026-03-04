/**
 * RegisterPage — name, email, password, role selection.
 */

import React, { useState } from "react";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import {
  Box,
  Paper,
  Stack,
  TextField,
  Typography,
  Button,
  Alert,
  Link,
  MenuItem,
  InputAdornment,
  IconButton,
} from "@mui/material";
import {
  Visibility,
  VisibilityOff,
  TrendingUp as LogoIcon,
} from "@mui/icons-material";
import { useAuthStore } from "../../store/authStore";

export function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Investor");
  const [showPw, setShowPw] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState(null);
  const [severity, setSeverity] = useState("success");
  const register = useAuthStore((s) => s.register);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !email || !password) { setMessage("Please fill in all fields."); setSeverity("error"); return; }
    if (password.length < 8) { setMessage("Password must be at least 8 characters."); setSeverity("error"); return; }
    setSubmitting(true);
    setMessage(null);
    try {
      await register({ name, email, password, role });
      setMessage("Account created! Redirecting to login…");
      setSeverity("success");
      setTimeout(() => navigate("/login"), 1500);
    } catch {
      setMessage("Registration failed. Email may already be in use.");
      setSeverity("error");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box sx={{ width: "100%", maxWidth: 420 }}>
      <Box sx={{ textAlign: "center", mb: 4 }}>
        <Box
          sx={{
            width: 56, height: 56, borderRadius: 3, mx: "auto", mb: 2,
            background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
            display: "flex", alignItems: "center", justifyContent: "center",
            boxShadow: "0 0 40px rgba(99,102,241,0.3)",
          }}
        >
          <LogoIcon sx={{ color: "#fff", fontSize: 28 }} />
        </Box>
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 0.5 }}>
          Create account
        </Typography>
        <Typography color="text.secondary">
          Join ERIMS to manage equity risk
        </Typography>
      </Box>

      <Paper
        component="form"
        onSubmit={handleSubmit}
        sx={{ p: 4, borderRadius: 3, background: "linear-gradient(180deg, rgba(17,24,39,1) 0%, rgba(17,24,39,0.8) 100%)" }}
      >
        <Stack spacing={2.5}>
          {message && <Alert severity={severity} variant="filled" sx={{ borderRadius: 2 }}>{message}</Alert>}

          <TextField
            id="register-name"
            label="Full name"
            fullWidth
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoFocus
          />

          <TextField
            id="register-email"
            label="Email address"
            type="email"
            fullWidth
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
          />

          <TextField
            id="register-password"
            label="Password"
            type={showPw ? "text" : "password"}
            fullWidth
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            helperText="Minimum 8 characters"
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton size="small" onClick={() => setShowPw(!showPw)} edge="end">
                    {showPw ? <VisibilityOff fontSize="small" /> : <Visibility fontSize="small" />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />

          <TextField
            id="register-role"
            select
            label="Role"
            fullWidth
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <MenuItem value="Investor">Investor</MenuItem>
            <MenuItem value="Analyst">Analyst</MenuItem>
          </TextField>

          <Button
            id="register-submit"
            type="submit"
            variant="contained"
            size="large"
            disabled={submitting}
            sx={{ py: 1.4, fontSize: "1rem", borderRadius: 2.5 }}
          >
            {submitting ? "Creating account…" : "Create account"}
          </Button>

          <Typography variant="body2" sx={{ textAlign: "center", color: "text.secondary" }}>
            Already have an account?{" "}
            <Link component={RouterLink} to="/login" sx={{ fontWeight: 600, color: "primary.main" }}>
              Sign in
            </Link>
          </Typography>
        </Stack>
      </Paper>
    </Box>
  );
}
