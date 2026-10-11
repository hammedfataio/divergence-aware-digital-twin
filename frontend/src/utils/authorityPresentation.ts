import type { Authority } from "../types/api";

export interface AuthorityPresentation {
  label: string;
  description: string;
  action: string;
  textClass: string;
  borderClass: string;
  backgroundClass: string;
  glowClass: string;
}

export function authorityPresentation(
  authority: Authority,
): AuthorityPresentation {
  switch (authority) {
    case "allow":
      return {
        label: "APPROVED",
        description: "AI can proceed",
        action: "No human action required",
        textClass: "text-emerald-300",
        borderClass: "border-emerald-400/20",
        backgroundClass: "bg-emerald-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(52,211,153,0.10)]",
      };
    case "restrict":
      return {
        label: "LIMITED",
        description: "Proceed within restrictions",
        action: "Operator awareness required",
        textClass: "text-amber-300",
        borderClass: "border-amber-400/20",
        backgroundClass: "bg-amber-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(251,191,36,0.10)]",
      };
    case "defer":
      return {
        label: "WAITING",
        description: "More reliable information is needed",
        action: "Review information before proceeding",
        textClass: "text-orange-300",
        borderClass: "border-orange-400/20",
        backgroundClass: "bg-orange-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(251,146,60,0.10)]",
      };
    case "fallback":
      return {
        label: "SAFE MODE",
        description: "Use backup behaviour",
        action: "AI decision replaced by fallback behaviour",
        textClass: "text-red-300",
        borderClass: "border-red-400/20",
        backgroundClass: "bg-red-400/[0.07]",
        glowClass: "shadow-[0_0_55px_rgba(248,113,113,0.10)]",
      };
  }
}
