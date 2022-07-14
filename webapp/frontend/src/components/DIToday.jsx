import React from 'react';
import Box from "@material-ui/core/Box";
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

import MyLineChart from "./MyLineChart";

export const DIToday = () => (
  <Container maxWidth="md">
    <Box>
      <Paper>
        <Box p={2}>
          <Box>
            <Typography variant="h6">
              CDI
            </Typography>
            <Typography variant="subtitle2">
              CDI de acordo com o tempo
            </Typography>
          </Box>
          <MyLineChart/>
        </Box>
      </Paper>
    </Box>
  </Container>
);

const getDI = () => "1.90";

export default DIToday;
