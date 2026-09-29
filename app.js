function showLoading() {

    const button =
        document.getElementById(
            "generateBtn"
        );

    const loading =
        document.getElementById(
            "loading"
        );


    if (button) {

        button.disabled = true;

        button.textContent =
            "Creating…";

    }


    if (loading) {

        loading.classList.remove(
            "hidden"
        );

    }
}


async function downloadComic(exportId) {

    try {

        const response =
            await fetch(
                `/download/${encodeURIComponent(exportId)}`
            );


        if (!response.ok) {

            throw new Error(
                "PDF export could not be downloaded."
            );

        }


        const blob =
            await response.blob();


        const url =
            URL.createObjectURL(blob);


        const link =
            document.createElement("a");


        link.href = url;


        link.download =
            `comic-${exportId}.pdf`;


        document.body.appendChild(
            link
        );


        link.click();


        link.remove();


        URL.revokeObjectURL(url);


        window.location.href =
            "/export-success";


    } catch (error) {

        alert(error.message);

    }
}