/**
 * RiskDashboardPage — portfolio selector, risk assessments, charts.
 */

import React, { useEffect, useState, useCallback } from "react";
import {
  Box,
  Typography,
  Paper,
  MenuItem,
  TextField,
  Button,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  TableContainer,
  Chip,
  Grid,
  alpha,
  CircularProgress,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stack,
} from "@mui/material";
import {
  Assessment as RiskIcon,
  Speed as GaugeIcon,
  BarChart as BarIcon,
} from "@mui/icons-material";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { usePortfolioStore } from "../../store/portfolioStore";
import { useRiskStore } from "../../store/riskStore";

const CHART_COLORS = ["#6366f1", "#8b5cf6", "#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#ec4899", "#14b8a6"];

function getScoreColor(score) {
  if (score >= 70) return "#ef4444";
  if (score >= 40) return "#f59e0b";
  return "#10b981";
}

function ScoreGauge({ score, label }) {
  const color = getScoreColor(score);
  return (
    <Box sx={{ textAlign: "center" }}>
      <Box sx={{ position: "relative", display: "inline-flex" }}>
        <CircularProgress
          variant="determinate"
          value={100}
          size={90}
          thickness={4}
          sx={{ color: alpha(color, 0.15), position: "absolute" }}
        />
        <CircularProgress
          variant="determinate"
          value={score}
          size={90}
          thickness={4}
          sx={{ color }}
        />
        <Box sx={{
          top: 0, left: 0, bottom: 0, right: 0, position: "absolute",
          display: "flex", alignItems: "center", justifyContent: "center",
        }}>
          <Typography variant="h5" sx={{ fontWeight: 800, color }}>
            {Math.round(score)}
          </Typography>
        </Box>
      </Box>
      <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: "block" }}>
        {label}
      </Typography>
    </Box>
  );
}

export function RiskDashboardPage() {
  const { portfolios, equities, loadPortfolios, loadEquities } = usePortfolioStore();
  const { assessments, metrics, loadMetrics, loadAssessments, assessEquity } = useRiskStore();
  const [selectedPortfolio, setSelectedPortfolio] = useState("");
  const [assessDialog, setAssessDialog] = useState(false);
  const [selectedEquity, setSelectedEquity] = useState(null);
  const [assessing, setAssessing] = useState(false);
  const [assessError, setAssessError] = useState(null);

  const initData = useCallback(() => {
    loadPortfolios();
    loadMetrics();
  }, [loadPortfolios, loadMetrics]);

  useEffect(() => { initData(); }, [initData]);

  const loadPortfolioData = useCallback(() => {
    if (selectedPortfolio) {
      loadEquities(selectedPortfolio);
      loadAssessments(selectedPortfolio);
    }
  }, [selectedPortfolio, loadEquities, loadAssessments]);

  useEffect(() => { loadPortfolioData(); }, [loadPortfolioData]);

  const handleAssess = async () => {
    if (!selectedEquity || metrics.length === 0) return;
    setAssessing(true);
    setAssessError(null);
    try {
      await assessEquity({
        equity_id: selectedEquity.equity_id,
        metric_id: metrics[0].metric_id,
        analyst_id: 0,
        risk_score: 0,
      });
      await loadAssessments(selectedPortfolio);
      setAssessDialog(false);
    } catch (err) {
      setAssessError(err?.response?.data?.detail || "Assessment failed. Ensure market data is available.");
    }
    setAssessing(false);
  };

  // Build chart data
  const barData = assessments.map((a) => {
    const eq = equities.find((e) => e.equity_id === a.equity_id);
    return { name: eq?.company_name || `Eq #${a.equity_id}`, score: Number(a.risk_score) };
  });

  const sectorMap = {};
  equities.forEach((eq) => {
    const s = eq.sector || "Unknown";
    sectorMap[s] = (sectorMap[s] || 0) + (Number.parseFloat(eq.market_value) || 0);
  });
  const pieData = Object.entries(sectorMap).map(([name, value]) => ({ name, value }));

  const avgScore = assessments.length > 0
    ? assessments.reduce((s, a) => s + Number(a.risk_score), 0) / assessments.length
    : 0;

  return (
    <Box>
      <Typography variant="h4" sx={{ mb: 0.5 }}>Risk Dashboard</Typography>
      <Typography color="text.secondary" sx={{ mb: 3 }}>
        Assess equity risk and monitor portfolio exposure
      </Typography>

      {/* Portfolio selector */}
      <Paper sx={{ p: 3, mb: 3, borderRadius: 3 }}>
        <TextField
          id="risk-portfolio-select"
          select
          label="Select Portfolio"
          value={selectedPortfolio}
          onChange={(e) => setSelectedPortfolio(e.target.value)}
          sx={{ minWidth: 300 }}
        >
          {portfolios.map((p) => (
            <MenuItem key={p.portfolio_id} value={p.portfolio_id}>
              {p.portfolio_name}
            </MenuItem>
          ))}
        </TextField>
      </Paper>

      {!selectedPortfolio && (
        <Box sx={{ textAlign: "center", py: 10, border: "2px dashed", borderColor: (t) => alpha(t.palette.primary.main, 0.15), borderRadius: 3 }}>
          <RiskIcon sx={{ fontSize: 48, color: "text.secondary", mb: 2 }} />
          <Typography color="text.secondary">Select a portfolio to view risk analysis</Typography>
        </Box>
      )}

      {selectedPortfolio && (
        <>
          {/* Summary cards */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={4}>
              <Paper sx={{ p: 3, borderRadius: 3, textAlign: "center" }}>
                <ScoreGauge score={avgScore} label="Avg Risk Score" />
              </Paper>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Paper sx={{ p: 3, borderRadius: 3, textAlign: "center" }}>
                <Box sx={{ width: 42, height: 42, borderRadius: 2, mx: "auto", mb: 1, bgcolor: (t) => alpha(t.palette.info.main, 0.12), display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <BarIcon sx={{ color: "info.main" }} />
                </Box>
                <Typography variant="h4" sx={{ fontWeight: 800 }}>{equities.length}</Typography>
                <Typography variant="body2" color="text.secondary">Equities</Typography>
              </Paper>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Paper sx={{ p: 3, borderRadius: 3, textAlign: "center" }}>
                <Box sx={{ width: 42, height: 42, borderRadius: 2, mx: "auto", mb: 1, bgcolor: (t) => alpha(t.palette.secondary.main, 0.12), display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <GaugeIcon sx={{ color: "secondary.main" }} />
                </Box>
                <Typography variant="h4" sx={{ fontWeight: 800 }}>{assessments.length}</Typography>
                <Typography variant="body2" color="text.secondary">Assessments</Typography>
              </Paper>
            </Grid>
          </Grid>

          {/* Charts */}
          <Grid container spacing={3} sx={{ mb: 3 }}>
            {barData.length > 0 && (
              <Grid item xs={12} md={7}>
                <Paper sx={{ p: 3, borderRadius: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>Risk Scores by Equity</Typography>
                  <ResponsiveContainer width="100%" height={280}>
                    <BarChart data={barData}>
                      <XAxis dataKey="name" tick={{ fill: "#94a3b8", fontSize: 11 }} />
                      <YAxis domain={[0, 100]} tick={{ fill: "#94a3b8" }} />
                      <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 8 }} />
                      <Bar dataKey="score" radius={[6, 6, 0, 0]}>
                        {barData.map((entry) => (
                          <Cell key={entry.name} fill={CHART_COLORS[barData.indexOf(entry) % CHART_COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>
            )}
            {pieData.length > 0 && (
              <Grid item xs={12} md={5}>
                <Paper sx={{ p: 3, borderRadius: 3 }}>
                  <Typography variant="h6" sx={{ mb: 2 }}>Sector Exposure</Typography>
                  <ResponsiveContainer width="100%" height={280}>
                    <PieChart>
                      <Pie data={pieData} cx="50%" cy="50%" innerRadius={55} outerRadius={90} dataKey="value" stroke="none">
                        {pieData.map((entry) => (
                          <Cell key={entry.name} fill={CHART_COLORS[pieData.indexOf(entry) % CHART_COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ backgroundColor: "#1e293b", border: "1px solid rgba(99,102,241,0.2)", borderRadius: 8 }} />
                      <Legend wrapperStyle={{ color: "#94a3b8", fontSize: 12 }} />
                    </PieChart>
                  </ResponsiveContainer>
                </Paper>
              </Grid>
            )}
          </Grid>

          {/* Equities table with assess buttons */}
          <Paper sx={{ borderRadius: 3, overflow: "hidden" }}>
            <Box sx={{ px: 3, py: 2, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
              <Typography variant="h6">Equity Risk Analysis</Typography>
            </Box>
            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Company</TableCell>
                    <TableCell>Sector</TableCell>
                    <TableCell align="right">Market Value</TableCell>
                    <TableCell align="center">Latest Score</TableCell>
                    <TableCell align="center">Action</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {equities.map((eq) => {
                    const eqAssessments = assessments.filter((a) => a.equity_id === eq.equity_id);
                    const latest = eqAssessments.length > 0 ? eqAssessments[eqAssessments.length - 1] : null;
                    const score = latest ? Number(latest.risk_score) : null;
                    return (
                      <TableRow key={eq.equity_id} hover>
                        <TableCell sx={{ fontWeight: 600 }}>{eq.company_name}</TableCell>
                        <TableCell>{eq.sector || "—"}</TableCell>
                        <TableCell align="right" sx={{ color: "success.main", fontWeight: 600 }}>
                          ${Number(eq.market_value || 0).toLocaleString()}
                        </TableCell>
                        <TableCell align="center">
                          {score != null ? (
                            <Chip
                              size="small"
                              label={score.toFixed(1)}
                              sx={{
                                fontWeight: 700,
                                bgcolor: (t) => alpha(
                                  score >= 70 ? t.palette.error.main : score >= 40 ? t.palette.warning.main : t.palette.success.main,
                                  0.15
                                ),
                                color: score >= 70 ? "error.main" : score >= 40 ? "warning.main" : "success.main",
                              }}
                            />
                          ) : (
                            <Typography variant="caption" color="text.secondary">Not assessed</Typography>
                          )}
                        </TableCell>
                        <TableCell align="center">
                          <Button
                            size="small"
                            variant="outlined"
                            onClick={() => { setSelectedEquity(eq); setAssessDialog(true); }}
                          >
                            Assess
                          </Button>
                        </TableCell>
                      </TableRow>
                    );
                  })}
                  {equities.length === 0 && (
                    <TableRow>
                      <TableCell colSpan={5} sx={{ textAlign: "center", py: 4, color: "text.secondary" }}>
                        No equities in this portfolio. Add equities from the Portfolio page.
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>

          {/* Assess Dialog */}
          <Dialog open={assessDialog} onClose={() => { setAssessDialog(false); setAssessError(null); }} maxWidth="sm" fullWidth>
            <DialogTitle sx={{ fontWeight: 700 }}>Run Risk Assessment</DialogTitle>
            <DialogContent>
              <Stack spacing={2} sx={{ mt: 1 }}>
                {assessError && <Alert severity="error">{assessError}</Alert>}
                <Typography>
                  Analyze <strong>{selectedEquity?.company_name}</strong> using market data to compute risk score, volatility, and exposure metrics.
                </Typography>
                {metrics.length === 0 && (
                  <Alert severity="warning">
                    No risk metrics available. The system needs default metrics to be seeded.
                  </Alert>
                )}
              </Stack>
            </DialogContent>
            <DialogActions sx={{ px: 3, pb: 2 }}>
              <Button onClick={() => { setAssessDialog(false); setAssessError(null); }}>Cancel</Button>
              <Button
                variant="contained"
                onClick={handleAssess}
                disabled={assessing || metrics.length === 0}
              >
                {assessing ? "Analyzing…" : "Run Assessment"}
              </Button>
            </DialogActions>
          </Dialog>
        </>
      )}
    </Box>
  );
}
