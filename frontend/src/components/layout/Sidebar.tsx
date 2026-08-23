"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navigation = [
    {
        name: "Dashboard",
        href: "/",
    },
    {
        name: "Candidates",
        href: "/candidates",
    },
    {
        name: "Jobs",
        href: "/jobs",
    },
    {
        name: "Matches",
        href: "/matches",
    },
];

export default function Sidebar() {
    const pathname = usePathname();

    return (
        <aside className="flex min-h-screen w-64 flex-col border-r bg-white">
            <div className="border-b px-6 py-5">
                <h1 className="text-lg font-bold text-slate-900">
                    Smart Resume
                </h1>
                <p className="text-sm text-slate-500">
                    Screener
                </p>
            </div>

            <nav className="flex-1 space-y-1 p-4">
                {navigation.map((item) => {
                    const active = pathname === item.href;

                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={`block rounded-lg px-4 py-3 text-sm font-medium ${
                                active
                                    ? "bg-slate-900 text-white"
                                    : "text-slate-600 hover:bg-slate-100"
                            }`}
                        >
                            {item.name}
                        </Link>
                    );
                })}
            </nav>
        </aside>
    );
}