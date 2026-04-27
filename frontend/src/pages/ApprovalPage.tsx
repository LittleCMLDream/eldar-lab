import React, { useState, useEffect } from "react";
import { PendingRequest } from "@/lib/types";
import api from "@/lib/api";
export const ApprovalPage: React.FC = () => {
  const [requests, setRequests] = useState<PendingRequest[]>([]);
  const [loading, setLoading] = useState(true);
  useEffect(() => { api.get("/bookings").then((r) => setRequests(r.data.filter((b: any) => b.status === "pending"))).finally(() => setLoading(false)); }, []);
  const handleAction = async (id: number, action: string) => {
    await api.put(`/bookings/${id}/${action}`);
    setRequests((prev) => prev.filter((r) => r.id !== id));
  };
  if (loading) return <p className="text-gray-500">Loading...</p>;
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">审批管理</h2>
      {requests.length === 0 ? <p className="text-gray-400">暂无待审批申请</p> : (
        <table className="w-full border-collapse bg-white rounded-lg overflow-hidden shadow">
          <thead className="bg-gray-100">
            <tr>{["单号","课程","班级","事由","操作"].map(h => <th key={h} className="border px-4 py-2 text-sm font-medium">{h}</th>)}</tr>
          </thead>
          <tbody>
            {requests.map((r) => (
              <tr key={r.id} className="text-sm">
                <td className="border px-4 py-2">{r.request_no}</td>
                <td className="border px-4 py-2">{r.course_name}</td>
                <td className="border px-4 py-2">{r.class_names}</td>
                <td className="border px-4 py-2">{r.reason}</td>
                <td className="border px-4 py-2 text-center">
                  <button onClick={() => handleAction(r.id, "approve")} className="px-3 py-1 mr-2 bg-green-600 text-white rounded text-xs hover:bg-green-700">同意</button>
                  <button onClick={() => handleAction(r.id, "reject")} className="px-3 py-1 bg-red-600 text-white rounded text-xs hover:bg-red-700">拒绝</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
