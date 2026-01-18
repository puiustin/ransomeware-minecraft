import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    
    console.log("---------- RECEIVED VICTIM ----------");
    console.log(JSON.stringify(data, null, 2));
    console.log("-------------------------------------");

    return NextResponse.json({ status: 'success', message: 'victim received' });
  } catch (error) {
    console.error("Error processing victim:", error);
    return NextResponse.json({ status: 'error', message: 'Invalid request' }, { status: 400 });
  }
}
