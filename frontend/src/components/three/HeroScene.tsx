"use client";

import { Canvas, useFrame, useThree } from "@react-three/fiber";
import { Float, Icosahedron, MeshDistortMaterial, Torus } from "@react-three/drei";
import { useEffect, useMemo, useRef, useState } from "react";
import * as THREE from "three";

/**
 * The hero object: a refracting core inside two counter-rotating rings, wrapped
 * in a slow particle field. Everything is procedural — no textures or HDRIs are
 * fetched, so the scene paints on first frame.
 */

function ParticleField({ count = 700 }: { count?: number }) {
  const points = useRef<THREE.Points>(null);

  const positions = useMemo(() => {
    // Seeded so the field is identical on every render and between reloads.
    let seed = 0x9e3779b9;
    const random = () => {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      return seed / 0xffffffff;
    };
    const array = new Float32Array(count * 3);
    for (let i = 0; i < count; i += 1) {
      // Even-ish shell distribution so the core stays visible in the middle.
      const radius = 3.2 + random() * 5.5;
      const theta = random() * Math.PI * 2;
      const phi = Math.acos(2 * random() - 1);
      array[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      array[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta) * 0.6;
      array[i * 3 + 2] = radius * Math.cos(phi);
    }
    return array;
  }, [count]);

  useFrame((_, delta) => {
    if (!points.current) return;
    points.current.rotation.y += delta * 0.035;
    points.current.rotation.x += delta * 0.012;
  });

  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial
        size={0.035}
        color="#a5b4ff"
        transparent
        opacity={0.75}
        sizeAttenuation
        depthWrite={false}
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}

function Core() {
  const shell = useRef<THREE.Mesh>(null);
  const ringA = useRef<THREE.Mesh>(null);
  const ringB = useRef<THREE.Mesh>(null);

  useFrame((state, delta) => {
    const t = state.clock.elapsedTime;
    if (shell.current) {
      shell.current.rotation.y += delta * 0.12;
      shell.current.rotation.z = Math.sin(t * 0.2) * 0.12;
    }
    if (ringA.current) ringA.current.rotation.z += delta * 0.25;
    if (ringB.current) ringB.current.rotation.x -= delta * 0.18;
  });

  return (
    <group>
      <Float speed={1.4} rotationIntensity={0.35} floatIntensity={0.9}>
        <Icosahedron args={[1.55, 12]}>
          <MeshDistortMaterial
            color="#6d5efc"
            emissive="#3d2fa8"
            emissiveIntensity={0.55}
            roughness={0.12}
            metalness={0.85}
            distort={0.34}
            speed={1.6}
          />
        </Icosahedron>

        <mesh ref={shell} scale={1.92}>
          <icosahedronGeometry args={[1.55, 1]} />
          <meshBasicMaterial color="#7f8bff" wireframe transparent opacity={0.16} />
        </mesh>
      </Float>

      <Torus ref={ringA} args={[2.9, 0.012, 16, 128]} rotation={[Math.PI / 2.6, 0, 0]}>
        <meshBasicMaterial color="#22d3ee" transparent opacity={0.55} />
      </Torus>
      <Torus ref={ringB} args={[3.55, 0.008, 16, 128]} rotation={[0, Math.PI / 3, Math.PI / 5]}>
        <meshBasicMaterial color="#e879f9" transparent opacity={0.4} />
      </Torus>
    </group>
  );
}

function PointerParallax() {
  const { camera, pointer } = useThree();
  /* eslint-disable react-hooks/immutability -- r3f drives the camera by mutation */
  useFrame(() => {
    camera.position.x += (pointer.x * 1.1 - camera.position.x) * 0.03;
    camera.position.y += (pointer.y * 0.7 - camera.position.y) * 0.03;
    camera.lookAt(0, 0, 0);
  });
  /* eslint-enable react-hooks/immutability */
  return null;
}

export default function HeroScene() {
  const [enabled, setEnabled] = useState(true);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      // Some embedded viewports report 0 here; only a real measurement counts as mobile.
      const width = window.innerWidth || document.documentElement.clientWidth;
      const small = width > 0 && width < 768;
      setEnabled(!reduced && !small);
    });
    return () => cancelAnimationFrame(frame);
  }, []);

  if (!enabled) {
    return (
      <div aria-hidden className="relative size-full">
        <div className="animate-pulse-soft absolute inset-[18%] rounded-full bg-linear-to-br from-violet-500 via-fuchsia-400 to-cyan-400 opacity-45 blur-3xl" />
        <div className="absolute inset-[32%] rounded-full border border-white/15" />
      </div>
    );
  }

  return (
    <Canvas
      aria-hidden
      dpr={[1, 1.75]}
      camera={{ position: [0, 0, 7.2], fov: 45 }}
      gl={{ antialias: true, alpha: true }}
      // Paint one frame immediately: a tab opened in the background gets no
      // rAF ticks, and an empty canvas would look like a broken hero.
      onCreated={({ gl, scene, camera }) => gl.render(scene, camera)}
      className="!absolute inset-0"
    >
      <ambientLight intensity={0.6} />
      <pointLight position={[6, 5, 6]} intensity={90} color="#8b7dff" />
      <pointLight position={[-6, -3, 4]} intensity={60} color="#22d3ee" />
      <pointLight position={[0, 6, -6]} intensity={45} color="#e879f9" />
      <Core />
      <ParticleField />
      <PointerParallax />
    </Canvas>
  );
}
