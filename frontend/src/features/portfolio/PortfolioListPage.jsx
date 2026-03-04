/**
 * TLDR; Portfolio list/management UI scaffold.
 * TODO: Implement portfolio CRUD and equity management per SRS FR2/FR3.
 */

import React, { useEffect, useState } from "react";
import { Paper, Stack, Typography, Button, TextField, List, ListItem, ListItemText } from "@mui/material";
import { httpClient } from "../../api/httpClient";
import { endpoints } from "../../api/endpoints";

export function PortfolioListPage() {
  const [portfolios, setPortfolios] = useState([]);
  const [newName, setNewName] = useState("");
  const [newDescription, setNewDescription] = useState("");

  const loadPortfolios = async () => {
    const { data } = await httpClient.get(endpoints.portfolios);
    setPortfolios(data);
  };

  useEffect(() => {
    loadPortfolios().catch(() => {});
  }, []);

  const handleCreate = async (event) => {
    event.preventDefault();
    await httpClient.post(endpoints.portfolios, {
      portfolio_name: newName,
      description: newDescription
    });
    setNewName("");
    setNewDescription("");
    await loadPortfolios();
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="h5">Portfolios</Typography>
      </Stack>
      <Stack
        component="form"
        onSubmit={handleCreate}
        direction="row"
        spacing={2}
        sx={{ mt: 2 }}
        alignItems="center"
      >
        <TextField
          size="small"
          label="Name"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
        />
        <TextField
          size="small"
          label="Description"
          value={newDescription}
          onChange={(e) => setNewDescription(e.target.value)}
        />
        <Button type="submit" variant="contained">
          New portfolio
        </Button>
      </Stack>
      <List sx={{ mt: 2 }}>
        {portfolios.map((p) => (
          <ListItem key={p.portfolio_id} divider>
            <ListItemText
              primary={p.portfolio_name}
              secondary={p.description || "No description"}
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
}

