import React from 'react';
import { LineChart, CartesianGrid, Line, Tooltip, ResponsiveContainer, XAxis, YAxis } from 'recharts';

const data = [
  {date: '2020-12-01', di: 0.001},
  {date: '2020-12-02', di: 0.002},
  {date: '2020-12-04', di: 0.003},
  {date: '2020-12-05', di: 0.004},
  {date: '2020-12-06', di: 0.005},
  {date: '2020-12-07', di: 0.002},
  {date: '2020-12-08', di: 0.001},
  {date: '2020-12-09', di: 0.0001},
  {date: '2020-12-10', di: 0.003},
  {date: '2020-12-11', di: 0.004},
  {date: '2020-12-12', di: 0.007},
  {date: '2020-12-13', di: 0.01},
  {date: '2020-12-14', di: 0.007},
  {date: '2020-12-15', di: 0.006},
  {date: '2020-12-16', di: 0.005},
  {date: '2020-12-17', di: 0.006},
  {date: '2020-12-18', di: 0.01},
  {date: '2020-12-19', di: 0.012},
  {date: '2020-12-20', di: 0.009},

];

export const MyLineChart = () => (
  <ResponsiveContainer height={300}>
    <LineChart data={data}>
      <Line type="monotone" dataKey="di" />
      <CartesianGrid stroke="#eee" strokeDasharray="10 10"/>
      <XAxis dataKey="date" />
      <YAxis/>
      <Tooltip />
    </LineChart>
  </ResponsiveContainer>
);

export default MyLineChart;
