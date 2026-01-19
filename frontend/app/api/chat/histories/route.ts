import { NextResponse } from "next/server";
import { getKindeServerSession } from "@kinde-oss/kinde-auth-nextjs/server";

export async function GET() {
    const { getUser } = getKindeServerSession();
    const user = await getUser();

    if (!user) {
        return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/chat/histories`,
        {
            headers: {
                "X-User-Id": user.id,
            },
        }
    );

    return NextResponse.json(await res.json());
}
