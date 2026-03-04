/**
 * App shell — sidebar navigation + top bar + content area.
 */

import React, { useEffect, useCallback } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  Box,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  IconButton,
  Avatar,
  Tooltip,
  Divider,
  alpha,
} from "@mui/material";
import {
  AccountBalanceWallet as PortfolioIcon,
  Assessment as RiskIcon,
  Summarize as ReportsIcon,
  Logout as LogoutIcon,
  TrendingUp as LogoIcon,
} from "@mui/icons-material";
import { useAuthStore } from "../store/authStore";

const DRAWER_WIDTH = 260;

const NAV_ITEMS = [
  { label: "Portfolios", path: "/portfolios", icon: <PortfolioIcon /> },
  { label: "Risk Dashboard", path: "/risk", icon: <RiskIcon /> },
  { label: "Reports", path: "/reports", icon: <ReportsIcon /> },
];

export function AppLayout({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const accessToken = useAuthStore((s) => s.accessToken);
  const currentUser = useAuthStore((s) => s.currentUser);
  const logout = useAuthStore((s) => s.logout);
  const loadCurrentUser = useAuthStore((s) => s.loadCurrentUser);

  const isAuthPage = ["/login", "/register"].includes(location.pathname);
  const showSidebar = accessToken && !isAuthPage;

  const handleLoadUser = useCallback(() => {
    if (accessToken && !currentUser) {
      loadCurrentUser().catch(() => {
        logout();
        navigate("/login");
      });
    }
  }, [accessToken, currentUser, loadCurrentUser, logout, navigate]);

  useEffect(() => {
    handleLoadUser();
  }, [handleLoadUser]);

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!showSidebar) {
    return (
      <Box sx={{ minHeight: "100vh", bgcolor: "background.default", display: "flex", alignItems: "center", justifyContent: "center" }}>
        {children}
      </Box>
    );
  }

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", bgcolor: "background.default" }}>
      {/* Sidebar */}
      <Drawer
        variant="permanent"
        sx={{
          width: DRAWER_WIDTH,
          flexShrink: 0,
          "& .MuiDrawer-paper": { width: DRAWER_WIDTH, boxSizing: "border-box", bgcolor: "background.paper" },
        }}
      >
        {/* Logo */}
        <Box sx={{ px: 2.5, py: 2.5, display: "flex", alignItems: "center", gap: 1.5 }}>
          <Box
            sx={{
              width: 40, height: 40, borderRadius: 2,
              background: "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
              display: "flex", alignItems: "center", justifyContent: "center",
              boxShadow: "0 0 20px rgba(99,102,241,0.3)",
            }}
          >
            <LogoIcon sx={{ color: "#fff", fontSize: 22 }} />
          </Box>
          <Box>
            <Typography variant="subtitle1" sx={{ fontWeight: 800, color: "text.primary", lineHeight: 1.2, letterSpacing: "-0.02em" }}>
              ERIMS
            </Typography>
            <Typography variant="caption" sx={{ color: "text.secondary", fontSize: "0.65rem" }}>
              Risk Intelligence
            </Typography>
          </Box>
        </Box>

        <Divider sx={{ mx: 2, mb: 1 }} />

        {/* Nav Links */}
        <List sx={{ px: 1, flex: 1 }}>
          {NAV_ITEMS.map((item) => {
            const active = location.pathname.startsWith(item.path);
            return (
              <ListItemButton
                key={item.path}
                selected={active}
                onClick={() => navigate(item.path)}
                sx={{ mb: 0.5 }}
              >
                <ListItemIcon sx={{ minWidth: 40, color: active ? "primary.main" : "text.secondary" }}>
                  {item.icon}
                </ListItemIcon>
                <ListItemText
                  primary={item.label}
                  primaryTypographyProps={{ fontWeight: active ? 600 : 400, fontSize: "0.875rem" }}
                />
                {active && (
                  <Box sx={{ width: 4, height: 24, borderRadius: 2, bgcolor: "primary.main", position: "absolute", right: 0 }} />
                )}
              </ListItemButton>
            );
          })}
        </List>

        {/* User section */}
        <Divider sx={{ mx: 2 }} />
        <Box sx={{ p: 2, display: "flex", alignItems: "center", gap: 1.5 }}>
          <Avatar
            sx={{
              width: 36, height: 36,
              bgcolor: (t) => alpha(t.palette.primary.main, 0.15),
              color: "primary.main",
              fontSize: "0.85rem", fontWeight: 700,
            }}
          >
            {currentUser?.name?.charAt(0)?.toUpperCase() || "U"}
          </Avatar>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="body2" sx={{ fontWeight: 600, lineHeight: 1.2 }} noWrap>
              {currentUser?.name || "Loading…"}
            </Typography>
            <Typography variant="caption" sx={{ color: "text.secondary" }} noWrap>
              {currentUser?.role || ""}
            </Typography>
          </Box>
          <Tooltip title="Sign out">
            <IconButton size="small" onClick={handleLogout} sx={{ color: "text.secondary" }}>
              <LogoutIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      </Drawer>

      {/* Main content */}
      <Box component="main" sx={{ flexGrow: 1, p: 3, maxWidth: `calc(100vw - ${DRAWER_WIDTH}px)` }}>
        {children}
      </Box>
    </Box>
  );
}
