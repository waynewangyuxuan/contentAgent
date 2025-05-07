import { NextResponse } from "next/server"

export async function GET() {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"}/status`)

    if (!response.ok) {
      throw new Error(`Failed to fetch status: ${response.status}`)
    }

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    console.error("Error fetching status:", error)
    return NextResponse.json({ error: "Failed to fetch agent status" }, { status: 500 })
  }
}
