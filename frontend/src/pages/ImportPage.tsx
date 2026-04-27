import React, { useState } from "react";
import api from "@/lib/api";
export const ImportPage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>("idle");
  const [message, setMessage] = useState("");
  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    const formData = new FormData();
    formData.append("file", file);
    try {
      await api.post("/import/excel", formData, { headers: { "Content-Type": "multipart/form-data" } });
      setStatus("success"); setMessage("导入成功！");
    } catch (e: any) { setStatus("error"); setMessage(e.response?.data?.detail || "导入失败"); }
  };
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">课表导入</h2>
      <div className="bg-white p-6 rounded-lg shadow max-w-md">
        <p className="text-sm text-gray-500 mb-3">上传 Excel (.xlsx) 文件导入课程表数据。</p>
        <input type="file" accept=".xlsx,.xls" onChange={(e) => setFile(e.target.files?.[0] ?? null)} className="block w-full text-sm mb-4" />
        <button onClick={handleUpload} disabled={!file || status === "uploading"} className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50">
          {status === "uploading" ? "上传中..." : "上传并导入"}
        </button>
        {status === "success" && <p className="mt-3 text-green-600 text-sm">{message}</p>}
        {status === "error" && <p className="mt-3 text-red-600 text-sm">{message}</p>}
      </div>
    </div>
  );
};
