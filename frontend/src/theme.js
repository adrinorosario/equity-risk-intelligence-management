/**
 * Premium dark theme for ERIMS.
 * Deep navy/slate palette with vibrant indigo accents.
 */

import { createTheme, alpha } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: "#6366f1", light: "#818cf8", dark: "#4f46e5" },
    secondary: { main: "#8b5cf6", light: "#a78bfa", dark: "#7c3aed" },
    success: { main: "#10b981", light: "#34d399", dark: "#059669" },
    warning: { main: "#f59e0b", light: "#fbbf24", dark: "#d97706" },
    error: { main: "#ef4444", light: "#f87171", dark: "#dc2626" },
    info: { main: "#3b82f6", light: "#60a5fa", dark: "#2563eb" },
    background: {
      default: "#060911",
      paper: "#111827",
    },
    text: {
      primary: "#f1f5f9",
      secondary: "#94a3b8",
    },
    divider: alpha("#6366f1", 0.12),
  },
  typography: {
    fontFamily: "'Inter', 'Roboto', 'Helvetica Neue', Arial, sans-serif",
    h4: { fontWeight: 700, letterSpacing: "-0.02em" },
    h5: { fontWeight: 700, letterSpacing: "-0.01em" },
    h6: { fontWeight: 600 },
    subtitle1: { fontWeight: 600, color: "#94a3b8" },
    button: { fontWeight: 600, textTransform: "none" },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollbarWidth: "thin",
          scrollbarColor: "#1e293b #060911",
        },
      },
    },
    MuiPaper: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: {
          backgroundImage: "none",
          border: "1px solid rgba(99,102,241,0.08)",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 10, padding: "8px 20px" },
        contained: {
          boxShadow: "0 0 20px rgba(99,102,241,0.25)",
          "&:hover": { boxShadow: "0 0 30px rgba(99,102,241,0.4)" },
        },
      },
    },
    MuiTextField: {
      defaultProps: { variant: "outlined", size: "small" },
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": {
            borderRadius: 10,
            "& fieldset": { borderColor: "rgba(99,102,241,0.2)" },
            "&:hover fieldset": { borderColor: "rgba(99,102,241,0.4)" },
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          border: "1px solid rgba(99,102,241,0.08)",
          transition: "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
          "&:hover": {
            borderColor: "rgba(99,102,241,0.25)",
            transform: "translateY(-2px)",
            boxShadow: "0 8px 32px rgba(99,102,241,0.12)",
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600, borderRadius: 8 },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          border: "1px solid rgba(99,102,241,0.15)",
          boxShadow: "0 24px 48px rgba(0,0,0,0.4)",
        },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: { borderColor: "rgba(99,102,241,0.08)" },
        head: { fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", fontSize: "0.75rem", letterSpacing: "0.05em" },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: "1px solid rgba(99,102,241,0.08)",
          backgroundImage: "none",
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 10,
          margin: "2px 8px",
          "&.Mui-selected": {
            backgroundColor: "rgba(99,102,241,0.12)",
            "&:hover": { backgroundColor: "rgba(99,102,241,0.18)" },
          },
        },
      },
    },
  },
});

export default theme;
