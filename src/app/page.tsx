export default function Home() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-glass backdrop-blur-xl">
      <div className="text-center space-y-4 p-8 rounded-[var(--radius-modal)] shadow-glass">
        <h1 className="text-3xl font-space font-bold text-cyan">ANGEL.AI Dashboard</h1>
        <p className="font-inter">Backend API at <code>/api</code> • Metrics at <code>/metrics</code></p>
      </div>
    </main>
  );
}
