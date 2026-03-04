/**
 * ReportsPage — generate and view portfolio risk reports.
 */

import React, { useEffect, useState, useCallback } from "react";
import {
  Box,
  Typography,
  Paper,
  MenuItem,
  TextField,
  Button,
  Grid,
  Chip,
  alpha,
  CircularProgress,
  Alert,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableContainer,
  Divider,
} from "@mui/material";
import {
  Summarize as ReportIcon,
} from "@mui/icons-material";
import { httpClient } from "../../api/httpClient";
import { endpoints } from "../../api/endpoints";
import { usePortfolioStore } from "../../store/portfolioStore";

export function ReportsPage() {
  const { portfolios, equities, loadPortfolios, loadEquities } = usePortfolioStore();
  const [selectedPortfolio, setSelectedPortfolio] = useState("");
  const [reportType, setReportType] = useState("risk_summary");
  const [generating, setGenerating] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);

  const initPortfolios = useCallback(() => {
    loadPortfolios();
  }, [loadPortfolios]);

  useEffect(() => { initPortfolios(); }, [initPortfolios]);

  const loadPortfolioEquities = useCallback(() => {
    if (selectedPortfolio) {
      loadEquities(selectedPortfolio);
    }
  }, [selectedPortfolio, loadEquities]);

  useEffect(() => { loadPortfolioEquities(); }, [loadPortfolioEquities]);

  const handleGenerate = async () => {
    if (!selectedPortfolio) return;
    setGenerating(true);
    setError(null);
    try {
      const { data } = await httpClient.post(endpoints.reports.create, {
        portfolio_id: Number.parseInt(selectedPortfolio, 10),
        created_by_user_id: 0,
        report_type: reportType,
      });
      setReport(data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to generate report");
    }
    setGenerating(false);
  };

  const portfolio = portfolios.find((p) => p.portfolio_id === Number.parseInt(selectedPortfolio, 10));
  const totalPortfolioValue = equities.reduce((sum, e) => sum + (Number.parseFloat(e.market_value) || 0), 0);

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 0.5 }}>Reports</Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        Generate and export risk evaluation reports
      </Typography>

      {/* Controls */}
      <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
        <Box sx={{ display: "flex", gap: 2, alignItems: "center", flexWrap: "wrap" }}>
          <TextField
            id="report-portfolio-select"
            select
            label="Portfolio"
            value={selectedPortfolio}
            onChange={(e) => { setSelectedPortfolio(e.target.value); setReport(null); }}
            sx={{ minWidth: 260 }}
          >
            {portfolios.map((p) => (
              <MenuItem key={p.portfolio_id} value={p.portfolio_id}>
                {p.portfolio_name}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            id="report-type-select"
            select
            label="Report Type"
            value={reportType}
            onChange={(e) => setReportType(e.target.value)}
            sx={{ minWidth: 200 }}
          >
            <MenuItem value="risk_summary">Risk Summary</MenuItem>
            <MenuItem value="detailed_analysis">Detailed Analysis</MenuItem>
            <MenuItem value="portfolio_overview">Portfolio Overview</MenuItem>
          </TextField>

          <Button
            id="generate-report-btn"
            variant="contained"
            startIcon={generating ? <CircularProgress size={18} color="inherit" /> : <ReportIcon />}
            onClick={handleGenerate}
            disabled={!selectedPortfolio || generating}
            sx={{ px: 3 }}
          >
            {generating ? "Generating…" : "Generate Report"}
          </Button>
        </Box>
        {error && <Alert severity="error" sx={{ mt: 2 }}>{error}</Alert>}
      </Paper>

      {/* Generated report preview */}
      {report && portfolio && (
        <Paper sx={{ p: 4, mb: 3, borderRadius: 3 }}>
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
            <Box>
              <Typography variant="h5" sx={{ fontWeight: 700, mb: 0.5 }}>
                {reportType === "risk_summary" ? "Risk Summary Report" :
                 reportType === "detailed_analysis" ? "Detailed Analysis Report" :
                 "Portfolio Overview Report"}
              </Typography>
              <Typography color="text.secondary">
                {"Generated on "}{new Date().toLocaleDateString()}{" • "}{portfolio.portfolio_name}
              </Typography>
            </Box>
            <Chip label={`Report #${report.report_id}`} variant="outlined" />
          </Box>

          <Divider sx={{ mb: 3 }} />

          {/* Summary stats */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={6} sm={3}>
              <Paper sx={{ p: 2, borderRadius: 2, bgcolor: (t) => alpha(t.palette.primary.main, 0.06), textAlign: "center" }}>
                <Typography variant="h5" sx={{ fontWeight: 800, color: "primary.main" }}>
                  {equities.length}
                </Typography>
                <Typography variant="caption" color="text.secondary">Total Equities</Typography>
              </Paper>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Paper sx={{ p: 2, borderRadius: 2, bgcolor: (t) => alpha(t.palette.success.main, 0.06), textAlign: "center" }}>
                <Typography variant="h5" sx={{ fontWeight: 800, color: "success.main" }}>
                  ${totalPortfolioValue.toLocaleString()}
                </Typography>
                <Typography variant="caption" color="text.secondary">Total Value</Typography>
              </Paper>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Paper sx={{ p: 2, borderRadius: 2, bgcolor: (t) => alpha(t.palette.warning.main, 0.06), textAlign: "center" }}>
                <Typography variant="h5" sx={{ fontWeight: 800, color: "warning.main" }}>
                  {portfolio.risk_level || "N/A"}
                </Typography>
                <Typography variant="caption" color="text.secondary">Risk Level</Typography>
              </Paper>
            </Grid>
            <Grid item xs={6} sm={3}>
              <Paper sx={{ p: 2, borderRadius: 2, bgcolor: (t) => alpha(t.palette.info.main, 0.06), textAlign: "center" }}>
                <Typography variant="h5" sx={{ fontWeight: 800, color: "info.main" }}>
                  {new Set(equities.map((e) => e.sector).filter(Boolean)).size}
                </Typography>
                <Typography variant="caption" color="text.secondary">Sectors</Typography>
              </Paper>
            </Grid>
          </Grid>

          {/* Equity breakdown */}
          {equities.length > 0 && (
            <TableContainer>
              <Typography variant="h6" sx={{ mb: 1.5 }}>Equity Breakdown</Typography>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Company</TableCell>
                    <TableCell>Sector</TableCell>
                    <TableCell align="right">Market Value</TableCell>
                    <TableCell align="right">Weight</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {equities.map((eq) => {
                    const weight = totalPortfolioValue > 0
                      ? ((Number.parseFloat(eq.market_value) || 0) / totalPortfolioValue * 100)
                      : 0;
                    return (
                      <TableRow key={eq.equity_id}>
                        <TableCell sx={{ fontWeight: 600 }}>{eq.company_name}</TableCell>
                        <TableCell>{eq.sector || "—"}</TableCell>
                        <TableCell align="right" sx={{ color: "success.main" }}>
                          ${Number(eq.market_value || 0).toLocaleString()}
                        </TableCell>
                        <TableCell align="right">{weight.toFixed(1)}%</TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </TableContainer>
          )}
        </Paper>
      )}

      {/* No portfolio selected */}
      {!selectedPortfolio && (
        <Box sx={{ textAlign: "center", py: 10, border: "2px dashed", borderColor: (t) => alpha(t.palette.primary.main, 0.15), borderRadius: 3 }}>
          <ReportIcon sx={{ fontSize: 48, color: "text.secondary", mb: 2 }} />
          <Typography color="text.secondary">Select a portfolio to generate reports</Typography>
        </Box>
      )}
    </Box>
  );
}
