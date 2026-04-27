import React from "react";
export const Dashboard: React.FC = () => (
  <div>
    <h2 className="text-2xl font-bold mb-4">Dashboard</h2>
    <div className="grid grid-cols-3 gap-4">
      {[["实验室总数", "--"], ["待审批申请", "--"], ["本周预约", "--"]].map(([l, v]) => (
        <div key={l} className="bg-white p-6 rounded-lg shadow">
          <p className="text-gray-500 text-sm">{l}</p><p className="text-3xl font-bold mt-1">{v}</p>
        </div>
      ))}
    </div>
  </div>
);
