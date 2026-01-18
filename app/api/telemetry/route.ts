import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    console.log("-------- RECEIVED TELEMETRY ---------");
    console.log(JSON.stringify(data, null, 2));
    console.log("-------------------------------------");

    return NextResponse.json({ status: 'success', message: 'Telemetry received' });
  } catch (error) {
    console.error("Error processing telemetry:", error);
    return NextResponse.json({ status: 'error', message: 'Invalid request' }, { status: 400 });
  }
}
