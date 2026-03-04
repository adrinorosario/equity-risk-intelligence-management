/**
 * PortfolioDetailsPage — view portfolio + manage equities.
 */

import React, { useEffect, useState, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Button,
  Paper,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableContainer,
  IconButton,
  Tooltip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Stack,
  Chip,
  alpha,
  CircularProgress,
  Alert,
} from "@mui/material";
import {
  ArrowBack,
  Add as AddIcon,
  Delete as DeleteIcon,
  TrendingUp,
} from "@mui/icons-material";
import { usePortfolioStore } from "../../store/portfolioStore";

export function PortfolioDetailsPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const {
    currentPortfolio, equities, loading,
    loadPortfolio, loadEquities, addEquity, deleteEquity,
  } = usePortfolioStore();

  const [dialogOpen, setDialogOpen] = useState(false);
  const [form, setForm] = useState({ company_name: "", sector: "", market_value: "", exchange: "", purchase_date: "" });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = useCallback(() => {
    loadPortfolio(id);
    loadEquities(id);
  }, [id, loadPortfolio, loadEquities]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAdd = async () => {
    if (!form.company_name.trim()) return;
    setSubmitting(true);
    setError(null);
    try {
      await addEquity(Number.parseInt(id, 10), {
        company_name: form.company_name,
        sector: form.sector || null,
        market_value: Number.parseFloat(form.market_value) || 0,
        exchange: form.exchange || null,
        purchase_date: form.purchase_date || null,
      });
      setDialogOpen(false);
      setForm({ company_name: "", sector: "", market_value: "", exchange: "", purchase_date: "" });
    } catch {
      setError("Failed to add equity");
    }
    setSubmitting(false);
  };

  const handleDeleteEquity = async (equityId) => {
    if (globalThis.confirm("Remove this equity from the portfolio?")) {
      await deleteEquity(equityId);
    }
  };

  const totalValue = equities.reduce((sum, e) => sum + (Number.parseFloat(e.market_value) || 0), 0);

  if (loading && !currentPortfolio) {
    return <Box sx={{ textAlign: "center", py: 8 }}><CircularProgress /></Box>;
  }

  return (
    <Box>
      {/* Back + Header */}
      <Button
        startIcon={<ArrowBack />}
        onClick={() => navigate("/portfolios")}
        sx={{ mb: 2, color: "text.secondary" }}
      >
        Back to Portfolios
      </Button>

      <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
          <Box>
            <Typography variant="h4" sx={{ mb: 0.5 }}>
              {currentPortfolio?.portfolio_name || "Portfolio"}
            </Typography>
            <Typography color="text.secondary" sx={{ mb: 2 }}>
              {currentPortfolio?.description || "No description"}
            </Typography>
            <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
              <Chip
                icon={<TrendingUp />}
                label={`Total: $${totalValue.toLocaleString(undefined, { minimumFractionDigits: 2 })}`}
                sx={{ fontWeight: 700, bgcolor: (t) => alpha(t.palette.success.main, 0.12), color: "success.main" }}
              />
              <Chip label={`${equities.length} equities`} variant="outlined" />
              {currentPortfolio?.risk_level && (
                <Chip label={currentPortfolio.risk_level} color="warning" variant="outlined" />
              )}
            </Box>
          </Box>
          <Button
            id="add-equity-btn"
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setDialogOpen(true)}
          >
            Add Equity
          </Button>
        </Box>
      </Paper>

      {/* Equities Table */}
      {equities.length === 0 ? (
        <Box
          sx={{
            textAlign: "center", py: 8,
            border: "2px dashed", borderColor: (t) => alpha(t.palette.primary.main, 0.15),
            borderRadius: 3,
          }}
        >
          <Typography color="text.secondary" sx={{ mb: 1 }}>No equities yet</Typography>
          <Button variant="outlined" startIcon={<AddIcon />} onClick={() => setDialogOpen(true)}>
            Add Your First Equity
          </Button>
        </Box>
      ) : (
        <TableContainer component={Paper} sx={{ borderRadius: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Company</TableCell>
                <TableCell>Sector</TableCell>
                <TableCell>Exchange</TableCell>
                <TableCell align="right">Market Value</TableCell>
                <TableCell>Purchase Date</TableCell>
                <TableCell align="center">Actions</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {equities.map((eq) => (
                <TableRow key={eq.equity_id} hover>
                  <TableCell>
                    <Typography sx={{ fontWeight: 600 }}>{eq.company_name}</Typography>
                  </TableCell>
                  <TableCell>
                    {eq.sector ? <Chip size="small" label={eq.sector} variant="outlined" /> : "—"}
                  </TableCell>
                  <TableCell>{eq.exchange || "—"}</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 600, color: "success.main" }}>
                    ${Number(eq.market_value || 0).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                  </TableCell>
                  <TableCell>
                    {eq.purchase_date ? new Date(eq.purchase_date).toLocaleDateString() : "—"}
                  </TableCell>
                  <TableCell align="center">
                    <Tooltip title="Delete">
                      <IconButton
                        size="small"
                        onClick={() => handleDeleteEquity(eq.equity_id)}
                        sx={{ color: "text.secondary", "&:hover": { color: "error.main" } }}
                      >
                        <DeleteIcon fontSize="small" />
                      </IconButton>
                    </Tooltip>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}

      {/* Add Equity Dialog */}
      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ fontWeight: 700 }}>Add Equity</DialogTitle>
        <DialogContent>
          <Stack spacing={2.5} sx={{ mt: 1 }}>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField
              id="equity-company-input"
              label="Company name"
              fullWidth
              value={form.company_name}
              onChange={(e) => setForm({ ...form, company_name: e.target.value })}
              autoFocus
            />
            <TextField
              id="equity-sector-input"
              label="Sector"
              fullWidth
              value={form.sector}
              onChange={(e) => setForm({ ...form, sector: e.target.value })}
            />
            <TextField
              id="equity-value-input"
              label="Market value ($)"
              type="number"
              fullWidth
              value={form.market_value}
              onChange={(e) => setForm({ ...form, market_value: e.target.value })}
            />
            <TextField
              id="equity-exchange-input"
              label="Exchange"
              fullWidth
              value={form.exchange}
              onChange={(e) => setForm({ ...form, exchange: e.target.value })}
            />
            <TextField
              id="equity-date-input"
              label="Purchase date"
              type="date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={form.purchase_date}
              onChange={(e) => setForm({ ...form, purchase_date: e.target.value })}
            />
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button
            id="equity-add-submit"
            variant="contained"
            onClick={handleAdd}
            disabled={submitting || !form.company_name.trim()}
          >
            {submitting ? "Adding…" : "Add Equity"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
