/**
 * TLDR; Registration page UI scaffold.
 * TODO: Implement form, validation, and call backend `/auth/register`.
 */

import React from "react";
import { Paper, Stack, TextField, Typography, Button } from "@mui/material";

export function RegisterPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Stack spacing={2}>
        <Typography variant="h5">Create account</Typography>
        <TextField label="Name" fullWidth />
        <TextField label="Email" fullWidth />
        <TextField label="Password" type="password" fullWidth />
        <Button variant="contained">Register</Button>
      </Stack>
    </Paper>
  );
}

