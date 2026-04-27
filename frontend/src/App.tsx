import React from "react";
import { Routes, Route } from "react-router-dom";
import { Layout } from "./components/layout/Layout";
import { Dashboard } from "./pages/Dashboard";
import { BookingPage } from "./pages/BookingPage";
import { ApprovalPage } from "./pages/ApprovalPage";
import { ImportPage } from "./pages/ImportPage";
const App: React.FC = () => (
  <Routes>
    <Route path="/" element={<Layout />}>
      <Route index element={<Dashboard />} />
      <Route path="booking" element={<BookingPage />} />
      <Route path="approval" element={<ApprovalPage />} />
      <Route path="import" element={<ImportPage />} />
    </Route>
  </Routes>
);
export default App;
