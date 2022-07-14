import React from 'react';
import Box from "@material-ui/core/Box";
import CssBaseline from "@material-ui/core/CssBaseline";
import MyLineChart from "./components/MyLineChart";
import DIToday from "./components/DIToday";

function App() {
  return (
    <>
      <CssBaseline/>
      <Box mt={3}>
        <DIToday/>
        TopBox
      </Box>
    </>
  );
}

export default App;
