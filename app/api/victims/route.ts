import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    console.log('Received victim report:', data); 

    return NextResponse.json({ message: 'Report received' }, { status: 200 });
  } catch (error) {
    console.error('Error processing victim report:', error);
    return NextResponse.json({ message: 'Error processing request' }, { status: 500 });
  }
}
