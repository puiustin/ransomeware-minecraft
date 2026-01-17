import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    // In a real app, you might save this to a database.
    // For this demo, we'll just log it to the server console.
    console.log("----- RECEIVED TELEMETRY REPORT -----");
    console.log("Timestamp:", new Date().toISOString());
    console.log("Data:", JSON.stringify(data, null, 2));
    console.log("-------------------------------------");

    return NextResponse.json({ status: 'success', message: 'Report received' });
  } catch (error) {
    console.error("Error processing report:", error);
    return NextResponse.json({ status: 'error', message: 'Invalid request' }, { status: 400 });
  }
}
