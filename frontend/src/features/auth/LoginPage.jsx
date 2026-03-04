/**
 * LoginPage — premium centered card, email + password, redirects on success.
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
  InputAdornment,
  IconButton,
} from "@mui/material";
import {
  Visibility,
  VisibilityOff,
  TrendingUp as LogoIcon,
} from "@mui/icons-material";
import { useAuthStore } from "../../store/authStore";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email || !password) { setError("Please fill in all fields."); return; }
    setSubmitting(true);
    setError(null);
    try {
      await login(email, password);
      navigate("/portfolios", { replace: true });
    } catch {
      setError("Invalid email or password. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box sx={{ width: "100%", maxWidth: 420 }}>
      {/* Logo */}
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
          Welcome back
        </Typography>
        <Typography color="text.secondary">
          Sign in to your ERIMS account
        </Typography>
      </Box>

      <Paper
        component="form"
        onSubmit={handleSubmit}
        sx={{ p: 4, borderRadius: 3, background: "linear-gradient(180deg, rgba(17,24,39,1) 0%, rgba(17,24,39,0.8) 100%)" }}
      >
        <Stack spacing={2.5}>
          {error && <Alert severity="error" variant="filled" sx={{ borderRadius: 2 }}>{error}</Alert>}

          <TextField
            id="login-email"
            label="Email address"
            type="email"
            fullWidth
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
            autoFocus
          />

          <TextField
            id="login-password"
            label="Password"
            type={showPw ? "text" : "password"}
            fullWidth
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
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

          <Button
            id="login-submit"
            type="submit"
            variant="contained"
            size="large"
            disabled={submitting}
            sx={{ py: 1.4, fontSize: "1rem", borderRadius: 2.5 }}
          >
            {submitting ? "Signing in…" : "Sign in"}
          </Button>

          <Typography variant="body2" sx={{ textAlign: "center", color: "text.secondary" }}>
            {"Don't have an account? "}
            <Link component={RouterLink} to="/register" sx={{ fontWeight: 600, color: "primary.main" }}>
              Create one
            </Link>
          </Typography>
        </Stack>
      </Paper>
    </Box>
  );
}
