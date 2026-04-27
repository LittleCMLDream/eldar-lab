import React from "react";
import { Outlet, NavLink } from "react-router-dom";
const links = [
  { to: "/", label: "Dashboard", icon: "📊" },
  { to: "/booking", label: "实验室预约", icon: "📅" },
  { to: "/approval", label: "审批管理", icon: "✅" },
  { to: "/import", label: "课表导入", icon: "📤" },
];
export const Layout: React.FC = () => (
  <div className="flex h-screen bg-gray-50">
    <aside className="w-60 bg-white border-r shadow-sm flex flex-col">
      <div className="p-5 border-b">
        <h1 className="text-xl font-bold text-blue-700">ELDAR</h1>
        <p className="text-xs text-gray-400">AI 实验室资源管理平台</p>
      </div>
      <nav className="flex-1 p-3 space-y-1">
        {links.map((l) => (
          <NavLink key={l.to} to={l.to} end={l.to === "/"}
            className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition ${isActive ? "bg-blue-50 text-blue-700" : "text-gray-600 hover:bg-gray-100"}`}>
            <span>{l.icon}</span>{l.label}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t text-xs text-gray-400">© 2026 ELDAR</div>
    </aside>
    <main className="flex-1 overflow-auto">
      <div className="p-6 max-w-6xl mx-auto"><Outlet /></div>
    </main>
  </div>
);
