/**
 * TLDR; Registration page UI scaffold.
 * TODO: Implement form, validation, and call backend `/auth/register`.
 */

import React, { useState } from "react";
import { Paper, Stack, TextField, Typography, Button } from "@mui/material";
import { useAuthStore } from "../../store/authStore";

export function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState(null);
  const register = useAuthStore((state) => state.register);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    setMessage(null);
    try {
      await register({ name, email, password });
      setMessage("Registration successful. You can now log in.");
    } catch (err) {
      setMessage("Registration failed. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Paper sx={{ p: 3 }} component="form" onSubmit={handleSubmit}>
      <Stack spacing={2}>
        <Typography variant="h5">Create account</Typography>
        <TextField
          label="Name"
          fullWidth
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <TextField
          label="Email"
          fullWidth
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <TextField
          label="Password"
          type="password"
          fullWidth
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {message ? (
          <Typography color="text.secondary" variant="body2">
            {message}
          </Typography>
        ) : null}
        <Button type="submit" variant="contained" disabled={submitting}>
          {submitting ? "Registering..." : "Register"}
        </Button>
      </Stack>
    </Paper>
  );
}

