"use client";
import { useEffect, useRef, useState } from "react";

function useWS(url: string) {
  const [open, setOpen] = useState(false);
  const [msg, setMsg] = useState<any>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const retryRef = useRef(0);
  const hbRef = useRef<any>(null);
  const ping = () => { wsRef.current?.send('{"t":"ping"}'); hbRef.current=setTimeout(reconnect, 4000); };
  const reconnect = () => {
    try { wsRef.current?.close(); } catch {}
    const backoff = Math.min(1000 * (2 ** retryRef.current++), 15000);
    setTimeout(connect, backoff);
  };
  const connect = () => {
    const ws = new WebSocket(url); wsRef.current=ws;
    ws.onopen = () => { retryRef.current=0; setOpen(true); clearTimeout(hbRef.current); ping(); };
    ws.onmessage = (e) => { clearTimeout(hbRef.current); setMsg(e.data); ping(); };
    ws.onclose = () => { setOpen(false); reconnect(); };
    ws.onerror = () => { setOpen(false); reconnect(); };
  };
  useEffect(() => { connect(); return () => { clearTimeout(hbRef.current); wsRef.current?.close(); }; }, [url]);
  return { open, msg };
}

async function post(path: string, body: any, idem: string) {
  const res = await fetch(`http://localhost:8000${path}`, {
    method: "POST",
    headers: { "Content-Type":"application/json", "X-Idempotency-Key": idem },
    body: JSON.stringify(body)
  });
  return res.json();
}

export default function Home() {
  const { open } = useWS("ws://localhost:8000/ws");
  const [halt, setHalt] = useState(false);
  return (
    <main style={{padding:20,fontFamily:"Inter, sans-serif"}}>
      <h1>ANGEL.AI — Ultracon Control</h1>
      <p>WS: {open ? "connected" : "reconnecting..."}</p>
      <button onClick={async ()=>{
        const r = await post("/v1/risk/kill", {enabled: !halt}, crypto.randomUUID());
        setHalt(r.enabled);
      }}>{halt ? "Resume" : "Kill"} Trading</button>
      <button onClick={async ()=>{
        const r = await post("/v1/order", {client_order_id: crypto.randomUUID(), symbol:"BTC-USD", side:"BUY", qty:0.01}, crypto.randomUUID());
        alert(JSON.stringify(r));
      }}>Test Order</button>
    </main>
  );
}
