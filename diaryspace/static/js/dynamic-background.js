/**
 * Применяет сменяющийся фон к <body>.
 *
 * @param backgroundsPath префикс URL для фонов.
 * @param quantity количество файлов фонов.
 * @param delay время показа каждого фона, в секундах.
 */
function dynamicBackgroundSetup(element, backgroundsPath, quantity, delay) {
    let $bg = $(element);
    let index = 0;

    setInterval(() => {
        index++;
        if (index > quantity) {
            index = 1;
        }
        let newBackgroundUrl = backgroundsPath + index.toString();
        $bg.css("background-image", `url(${newBackgroundUrl})`);
    }, delay * 1000);

    $bg.css("background-image", `url(${backgroundsPath}/1)`);
}