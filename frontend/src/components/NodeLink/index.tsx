/*
 * index.tsx
 * Author: evan kirkiles
 * Created on: Tue Nov 07 2023
 * 2023 Yale SWE
 */
"use client";

import { hoveredNodeAtom } from "@/app/state";
import { useSetAtom } from "jotai";
import Link from "next/link";
import { ComponentProps, PropsWithChildren, useRef } from "react";
import s from "./NodeLink.module.scss";
import { ExtendedNodeObject } from "@/app/api/graph/utils";

interface NodeLinkProps extends PropsWithChildren {
  nodeType: "production" | "person";
  nodeId: number;
  onlyScroll?: boolean;
}

const FAKE_NODE_DATA: ExtendedNodeObject = {
  id: "...",
  _type: "none",
  name: "undefined",
  val: 1,
  x: 0,
  y: 0,
};

export default function NodeLink({
  nodeType,
  nodeId,
  children,
  onlyScroll,
  ...props
}: NodeLinkProps & Omit<ComponentProps<typeof Link>, "href">) {
  const linkRef = useRef<HTMLAnchorElement>(null);
  const setHoveredNode = useSetAtom(hoveredNodeAtom);
  const href = `/${
    nodeType === "production" ? "productions" : "people"
  }/${nodeId}`;
  const nodeGraphId = `${nodeType.substring(0, 4)}_${nodeId}`;

  return (
    <Link
      href={href}
      {...props}
      prefetch={false}
      className={`${props.className} ${s.node_link}`}
      onMouseEnter={() =>
        setHoveredNode({ ...FAKE_NODE_DATA, id: nodeGraphId })
      }
      onFocus={() => setHoveredNode({ ...FAKE_NODE_DATA, id: nodeGraphId })}
      onMouseLeave={() => setHoveredNode(undefined)}
      onBlur={() => setHoveredNode(undefined)}
      data-node-type={nodeType}
      onClick={
        onlyScroll
          ? () =>
              linkRef.current?.scrollIntoView({
                block: "center",
                behavior: "smooth",
              })
          : undefined
      }
      ref={linkRef}
    >
      {children}
    </Link>
  );
}
