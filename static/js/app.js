// =========================================
// InterSoft Lite - Efectos de la interfaz
// =========================================

document.addEventListener("DOMContentLoaded", () => {

    // Onda (ripple) al hacer clic en los botones
    document.querySelectorAll(".btn").forEach((boton) => {
        boton.addEventListener("click", (evento) => {
            const rect = boton.getBoundingClientRect();
            const tamano = Math.max(rect.width, rect.height);
            const onda = document.createElement("span");

            onda.className = "ripple";
            onda.style.width = onda.style.height = `${tamano}px`;
            onda.style.left = `${evento.clientX - rect.left - tamano / 2}px`;
            onda.style.top = `${evento.clientY - rect.top - tamano / 2}px`;

            boton.appendChild(onda);
            onda.addEventListener("animationend", () => onda.remove());
        });
    });

    // Botón con "cargando..." al enviar un formulario
    document.querySelectorAll("form").forEach((formulario) => {
        formulario.addEventListener("submit", () => {
            const boton = formulario.querySelector("button[type='submit']");
            if (boton) {
                boton.classList.add("cargando");
            }
        });
    });

    // Brillo que sigue al cursor
    document.querySelectorAll(".spotlight").forEach((tarjeta) => {
        tarjeta.addEventListener("mousemove", (evento) => {
            const rect = tarjeta.getBoundingClientRect();
            tarjeta.style.setProperty("--x", `${evento.clientX - rect.left}px`);
            tarjeta.style.setProperty("--y", `${evento.clientY - rect.top}px`);
        });
    });

    // Inclinación 3D de las tarjetas de estadísticas
    document.querySelectorAll("[data-tilt]").forEach((tarjeta) => {
        tarjeta.addEventListener("mousemove", (evento) => {
            const rect = tarjeta.getBoundingClientRect();
            const x = (evento.clientX - rect.left) / rect.width - 0.5;
            const y = (evento.clientY - rect.top) / rect.height - 0.5;
            tarjeta.style.transform =
                `perspective(800px) rotateX(${-y * 10}deg) rotateY(${x * 10}deg) translateY(-4px)`;
        });

        tarjeta.addEventListener("mouseleave", () => {
            tarjeta.style.transform = "";
        });
    });

    // Contadores animados
    document.querySelectorAll("[data-contador]").forEach((elemento) => {
        const final = parseInt(elemento.dataset.contador, 10) || 0;
        const duracion = 1200;
        const inicio = performance.now();

        const animar = (ahora) => {
            const progreso = Math.min((ahora - inicio) / duracion, 1);
            const suavizado = 1 - Math.pow(1 - progreso, 3);
            elemento.textContent = Math.round(final * suavizado);
            if (progreso < 1) {
                requestAnimationFrame(animar);
            }
        };

        requestAnimationFrame(animar);
    });

    // Las filas de las tablas aparecen en cascada
    document.querySelectorAll(".tabla tbody tr").forEach((fila, indice) => {
        fila.style.animationDelay = `${Math.min(indice * 45, 900)}ms`;
    });

    // Notificaciones: se cierran solas o con la X
    const cerrarToast = (toast) => {
        toast.classList.add("saliendo");
        toast.addEventListener("animationend", () => toast.remove(), { once: true });
    };

    document.querySelectorAll(".toast").forEach((toast) => {
        const temporizador = setTimeout(() => cerrarToast(toast), 4500);
        toast.querySelector(".toast-cerrar").addEventListener("click", () => {
            clearTimeout(temporizador);
            cerrarToast(toast);
        });
    });

    // Buscador en vivo para las tablas
    document.querySelectorAll("[data-filtro]").forEach((buscador) => {
        const tabla = document.getElementById(buscador.dataset.filtro);
        const contador = document.querySelector(`[data-contador-de="${buscador.dataset.filtro}"]`);
        if (!tabla) {
            return;
        }

        const filas = Array.from(tabla.querySelectorAll("tbody tr"));

        buscador.addEventListener("input", () => {
            const texto = buscador.value.trim().toLowerCase();
            let visibles = 0;

            filas.forEach((fila) => {
                const coincide = fila.textContent.toLowerCase().includes(texto);
                fila.style.display = coincide ? "" : "none";
                if (coincide) {
                    visibles++;
                }
            });

            if (contador) {
                contador.textContent = `${visibles} de ${filas.length}`;
            }
        });
    });

    // Menú en pantallas pequeñas
    const botonMenu = document.querySelector("[data-menu-toggle]");
    const menu = document.querySelector("[data-menu]");
    if (botonMenu && menu) {
        botonMenu.addEventListener("click", () => menu.classList.toggle("abierto"));
    }
});
