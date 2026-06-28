import { useState, useRef } from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/layout/Sidebar";
import Topbar from "../components/layout/Topbar";

export default function AppLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const menuButtonRef = useRef(null);

  const closeSidebar = () => {
    setIsSidebarOpen(false);
    requestAnimationFrame(() => {
      if (menuButtonRef.current) {
        menuButtonRef.current.focus();
      }
    });
  };

  return (
    <div className="flex h-screen bg-slate-900 text-slate-100 overflow-hidden relative">
      {/* Mobile Sidebar Backdrop */}
      {isSidebarOpen && (
        <div
          className="fixed inset-0 bg-slate-950/60 backdrop-blur-sm z-40 lg:hidden cursor-pointer"
          onClick={closeSidebar}
          aria-hidden="true"
        />
      )}

      {/* Sidebar Navigation */}
      <Sidebar isOpen={isSidebarOpen} onClose={closeSidebar} />

      {/* Main Area */}
      <div className="flex flex-col flex-1 overflow-hidden">
        {/* Top Header */}
        <Topbar
          isSidebarOpen={isSidebarOpen}
          onToggleSidebar={() => setIsSidebarOpen(prev => !prev)}
          menuButtonRef={menuButtonRef}
        />

        {/* Content Area */}
        <main className="flex-1 overflow-y-auto p-4 md:p-8 w-full">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
