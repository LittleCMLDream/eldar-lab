import React, { useState, useEffect } from "react";
import { Lab, Booking, BookingForm } from "@/lib/types";
import { TimeGrid } from "@/components/custom/TimeGrid";
import { BookingDialog } from "@/components/custom/BookingDialog";
import api from "@/lib/api";
export const BookingPage: React.FC = () => {
  const [labs, setLabs] = useState<Lab[]>([]);
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [week, setWeek] = useState(1);
  const [day, setDay] = useState(1);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [selectedLab, setSelectedLab] = useState<Lab | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState(0);
  const [loading, setLoading] = useState(true);
  
  const fetchData = async () => {
    setLoading(true);
    try {
      const [labsRes, bkRes] = await Promise.all([
        api.get("/labs"),
        api.get("/bookings", { params: { week, day } }),
      ]);
      setLabs(labsRes.data);
      // Transform booking data for TimeGrid
      const transformed: Booking[] = (bkRes.data || []).flatMap((b: any) => 
        (b.slots || []).map((s: any) => ({
          id: b.id, lab_id: s.lab_id, week: s.week_number, day: s.day_of_week,
          start: s.period_start, end: s.period_end,
          status: b.status === "approved" ? "occupied" : b.status === "pending" ? "pending" : "free",
          course_name: b.course_name
        }))
      );
      setBookings(transformed);
    } catch (e) { console.error(e); }
    finally { setLoading(false); }
  };
  
  useEffect(() => { fetchData(); }, [week, day]);
  
  const handleCellClick = (lab: Lab, period: number) => { setSelectedLab(lab); setSelectedPeriod(period); setDialogOpen(true); };
  
  const handleSubmit = async (data: BookingForm) => {
    try {
      await api.post("/bookings", {
        semester_id: 1, reason: data.reason, course_name: data.course, class_names: data.class,
        slots: [{ lab_id: selectedLab!.id, week_number: week, day_of_week: day, period_start: selectedPeriod, period_end: selectedPeriod }]
      });
      alert("✅ 申请已提交，等待审批");
      fetchData();
    } catch (e: any) {
      alert("❌ " + (e.response?.data?.detail || "提交失败，该时段可能已被占用"));
    }
    setDialogOpen(false);
  };
  
  if (loading) return <div className="flex items-center justify-center h-64"><p className="text-gray-400">加载中...</p></div>;
  
  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">📅 实验室预约</h2>
      <div className="flex gap-3 mb-4">
        <label className="flex items-center gap-2 text-sm">周次:
          <select className="border rounded px-2 py-1" value={week} onChange={(e) => setWeek(+e.target.value)}>
            {[...Array(20)].map((_, i) => <option key={i} value={i + 1}>第 {i + 1} 周</option>)}
          </select>
        </label>
        <label className="flex items-center gap-2 text-sm">星期:
          <select className="border rounded px-2 py-1" value={day} onChange={(e) => setDay(+e.target.value)}>
            {["周一","周二","周三","周四","周五","周六","周日"].map((d, i) => <option key={i} value={i + 1}>{d}</option>)}
          </select>
        </label>
      </div>
      <TimeGrid labs={labs} bookings={bookings} week={week} day={day} onClick={handleCellClick} />
      <BookingDialog open={dialogOpen} onClose={() => setDialogOpen(false)} lab={selectedLab} period={selectedPeriod} onSubmit={handleSubmit} />
    </div>
  );
};
