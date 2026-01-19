import { NextResponse } from "next/server";
import { getKindeServerSession } from "@kinde-oss/kinde-auth-nextjs/server";

import { CreateChatHistoryMessage } from "@/lib/types/chat";

export async function GET(request: Request, context: { params: Promise<{ id: string }> }) {
    const { id } = await context.params;

    const { getUser } = getKindeServerSession();
    const user = await getUser();

    if (!user) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    console.log("asdjfoiwejfoiwejf");

    const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat/history/${id}/messages`,
        {
            headers: {
                "X-User-Id": user.id,
            },
        }
    );

    return NextResponse.json(await res.json());
}

export async function POST(request: Request, context: { params: Promise<{ id: string }> }) {
    const { id } = await context.params;
    const messageData: CreateChatHistoryMessage = await request.json();

    const { getUser } = getKindeServerSession();
    const user = await getUser();

    if (!user) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat/history/${id}/messages`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": user.id,
            },
            body: JSON.stringify(messageData),
        }
    );

    return NextResponse.json(await res.json());
}