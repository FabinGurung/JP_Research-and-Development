"use client";

import { useCallback, useEffect, useRef, useState, type KeyboardEvent } from "react";
import { usePathname } from "next/navigation";
import { sitePath } from "@/components/site-path";

const hubNavItems = [
  { href: "/", label: "Hub" },
  { href: "/projects/", label: "Research directory" },
  { href: "/aec/", label: "AEC / Structural" },
  { href: "/hydropower/", label: "Hydropower" },
  { href: "/governance/", label: "Research records" },
] as const;

const aecNavItems = [
  ["/", "Hub"],
  ["/aec/", "AEC Overview"],
  ["/research", "Research"],
  ["/system", "Database System"],
  ["/prototype", "Structural Prototype"],
  ["/workflow", "Shared-Data Reuse"],
  ["/methodology-demo/", "Methodology Demo"],
  ["/structural-demo/", "Structural Solver"],
  ["/graph", "System Graph"],
  ["/evidence", "Evidence"],
  ["/thesis", "Thesis"],
] as const;

const aecRoutePrefixes = [
  "/aec",
  "/research",
  "/system",
  "/prototype",
  "/workflow",
  "/methodology-demo",
  "/structural-demo",
  "/graph",
  "/evidence",
  "/roadmap",
  "/thesis",
] as const;

export function MobileNavigation() {
  const pathname = usePathname();
  const basePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "";
  const localPath = basePath && pathname.startsWith(basePath)
    ? pathname.slice(basePath.length) || "/"
    : pathname;
  const isAecRoute = aecRoutePrefixes.some(
    (prefix) => localPath === prefix || localPath.startsWith(`${prefix}/`),
  );

  const trackRef = useRef<HTMLDivElement>(null);
  const [hasMore, setHasMore] = useState(true);

  const updateOverflowCue = useCallback(() => {
    const track = trackRef.current;
    if (!track) return;
    const remaining = track.scrollWidth - track.clientWidth - track.scrollLeft;
    setHasMore(remaining > 2);
  }, []);

  useEffect(() => {
    const track = trackRef.current;
    if (!track) return;
    track.scrollLeft = 0;
    const frame = requestAnimationFrame(updateOverflowCue);
    const resizeObserver = new ResizeObserver(updateOverflowCue);
    resizeObserver.observe(track);
    return () => {
      cancelAnimationFrame(frame);
      resizeObserver.disconnect();
    };
  }, [localPath, updateOverflowCue]);

  const handleKeyboardScroll = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.target !== event.currentTarget || (event.key !== "ArrowLeft" && event.key !== "ArrowRight")) return;
    event.preventDefault();
    const track = trackRef.current;
    if (!track) return;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    track.scrollBy({
      left: (event.key === "ArrowRight" ? 1 : -1) * Math.max(128, track.clientWidth * 0.56),
      behavior: reduceMotion ? "auto" : "smooth",
    });
  };

  return (
    <nav className={`primary-nav ${hasMore ? "has-overflow-right" : ""}`} aria-label={isAecRoute ? "AEC module navigation" : "Research hub navigation"}>
      <span className="sr-only" id="primary-nav-scroll-help">
        This navigation scrolls horizontally on small screens. Use touch, a trackpad, or the left and right arrow keys while the navigation row is focused.
      </span>
      <div
        className="nav-track"
        ref={trackRef}
        tabIndex={0}
        aria-describedby="primary-nav-scroll-help"
        onScroll={updateOverflowCue}
        onKeyDown={handleKeyboardScroll}
      >
        {isAecRoute
          ? aecNavItems.map(([href, label]) => (
              <a href={sitePath(href)} key={href} aria-current={localPath.replace(/\/$/, '') === href.replace(/\/$/, '') ? 'page' : undefined}>{label}</a>
            ))
          : hubNavItems.map((item) => (
              <a href={sitePath(item.href)} key={item.href} aria-current={localPath.replace(/\/$/, '') === item.href.replace(/\/$/, '') ? 'page' : undefined}>{item.label}</a>
            ))}
      </div>
      <span className="nav-overflow-cue" aria-hidden="true"><span>›</span></span>
    </nav>
  );
}
