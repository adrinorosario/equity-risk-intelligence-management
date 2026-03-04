/**
 * PortfolioListPage — card grid with create dialog.
 */

import React, { useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActionArea,
  Grid,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Stack,
  alpha,
  IconButton,
  Tooltip,
  CircularProgress,
} from "@mui/material";
import {
  Add as AddIcon,
  Delete as DeleteIcon,
  AccountBalanceWallet as WalletIcon,
  TrendingUp,
} from "@mui/icons-material";
import { usePortfolioStore } from "../../store/portfolioStore";

export function PortfolioListPage() {
  const navigate = useNavigate();
  const { portfolios, loading, loadPortfolios, createPortfolio, deletePortfolio } = usePortfolioStore();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [creating, setCreating] = useState(false);

  const fetchPortfolios = useCallback(() => {
    loadPortfolios();
  }, [loadPortfolios]);

  useEffect(() => { fetchPortfolios(); }, [fetchPortfolios]);

  const handleCreate = async () => {
    if (!newName.trim()) return;
    setCreating(true);
    try {
      await createPortfolio({ portfolio_name: newName, description: newDesc });
      setDialogOpen(false);
      setNewName("");
      setNewDesc("");
    } catch {
      // Error handled by store
    }
    setCreating(false);
  };

  const handleDelete = async (e, id) => {
    e.stopPropagation();
    if (globalThis.confirm("Delete this portfolio and all its equities?")) {
      await deletePortfolio(id);
    }
  };

  const riskColor = (level) => {
    if (!level) return "default";
    const l = level.toLowerCase();
    if (l === "low") return "success";
    if (l === "medium") return "warning";
    return "error";
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", mb: 4 }}>
        <Box>
          <Typography variant="h4">Portfolios</Typography>
          <Typography color="text.secondary" sx={{ mt: 0.5 }}>
            Manage your equity portfolios and track performance
          </Typography>
        </Box>
        <Button
          id="create-portfolio-btn"
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setDialogOpen(true)}
          sx={{ px: 3 }}
        >
          New Portfolio
        </Button>
      </Box>

      {/* Loading */}
      {loading && (
        <Box sx={{ textAlign: "center", py: 8 }}>
          <CircularProgress />
        </Box>
      )}

      {/* Empty state */}
      {!loading && portfolios.length === 0 && (
        <Box
          sx={{
            textAlign: "center", py: 10,
            border: "2px dashed",
            borderColor: (t) => alpha(t.palette.primary.main, 0.2),
            borderRadius: 3,
          }}
        >
          <WalletIcon sx={{ fontSize: 48, color: "text.secondary", mb: 2 }} />
          <Typography variant="h6" color="text.secondary">No portfolios yet</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            Create your first portfolio to get started
          </Typography>
          <Button variant="outlined" startIcon={<AddIcon />} onClick={() => setDialogOpen(true)}>
            Create Portfolio
          </Button>
        </Box>
      )}

      {/* Portfolio grid */}
      <Grid container spacing={3}>
        {portfolios.map((p) => (
          <Grid item xs={12} sm={6} md={4} key={p.portfolio_id}>
            <Card>
              <CardActionArea
                onClick={() => navigate(`/portfolios/${p.portfolio_id}`)}
                sx={{ p: 0 }}
              >
                <CardContent sx={{ p: 3 }}>
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 2 }}>
                    <Box
                      sx={{
                        width: 42, height: 42, borderRadius: 2,
                        bgcolor: (t) => alpha(t.palette.primary.main, 0.12),
                        display: "flex", alignItems: "center", justifyContent: "center",
                      }}
                    >
                      <TrendingUp sx={{ color: "primary.main" }} />
                    </Box>
                    <Tooltip title="Delete portfolio">
                      <IconButton
                        size="small"
                        onClick={(e) => handleDelete(e, p.portfolio_id)}
                        sx={{ color: "text.secondary", "&:hover": { color: "error.main" } }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </Box>

                  <Typography variant="h6" sx={{ mb: 0.5, fontWeight: 700 }}>
                    {p.portfolio_name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2, minHeight: 40 }}>
                    {p.description || "No description"}
                  </Typography>

                  <Box sx={{ display: "flex", gap: 1, alignItems: "center", flexWrap: "wrap" }}>
                    {p.total_value != null && (
                      <Chip
                        size="small"
                        label={`$${Number(p.total_value).toLocaleString()}`}
                        sx={{ fontWeight: 700, bgcolor: (t) => alpha(t.palette.success.main, 0.12), color: "success.main" }}
                      />
                    )}
                    {p.risk_level && (
                      <Chip size="small" label={p.risk_level} color={riskColor(p.risk_level)} variant="outlined" />
                    )}
                    {p.creation_date && (
                      <Typography variant="caption" color="text.secondary">
                        Created {new Date(p.creation_date).toLocaleDateString()}
                      </Typography>
                    )}
                  </Box>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Create dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 700 }}>Create New Portfolio</DialogTitle>
        <DialogContent>
          <Stack spacing={2.5} sx={{ mt: 1 }}>
            <TextField
              id="portfolio-name-input"
              label="Portfolio name"
              fullWidth
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              autoFocus
            />
            <TextField
              id="portfolio-desc-input"
              label="Description (optional)"
              fullWidth
              multiline
              rows={2}
              value={newDesc}
              onChange={(e) => setNewDesc(e.target.value)}
            />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            id="portfolio-create-submit"
            variant="contained"
            onClick={handleCreate}
            disabled={creating || !newName.trim()}
          >
            {creating ? "Creating…" : "Create"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
