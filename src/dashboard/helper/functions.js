const fn = {
    formatdate(
        d,
        options = {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
        }
    ) {
        try {
            return new Date(d * 1000).toLocaleDateString('en-MY', options);
        } catch (e) {
            return '';
        }
    },
    deepCopy(obj) {
        if (typeof obj !== 'object' || obj === null) {
            return obj;
        }

        if (obj instanceof Date) {
            return new Date(obj.getTime());
        }

        if (obj instanceof Array) {
            return obj.reduce((arr, item, i) => {
                arr[i] = fn.deepCopy(item);
                return arr;
            }, []);
        }

        if (obj instanceof Object) {
            return Object.keys(obj).reduce((newObj, key) => {
                newObj[key] = fn.deepCopy(obj[key]);
                return newObj;
            }, {});
        }
    },
    wrapCsvValue(val, formatFn) {
        let formatted = formatFn !== void 0 ? formatFn(val) : val;

        formatted = formatted === void 0 || formatted === null ? '' : String(formatted);

        formatted = formatted.split('"').join('""');

        return `"${formatted}"`;
    },

    exportTable(rows, columns, name, exportFile) {
        //example call
        //exporTable(rows, columns, "file1.csv",exportFile) exportfile tu import dari quasar.
        // naive encoding to csv format
        const content = [columns.map((col) => fn.wrapCsvValue(col.label))]
            .concat(
                rows.map((row) =>
                    columns
                        .map((col) =>
                            fn.wrapCsvValue(
                                typeof col.field === 'function'
                                    ? col.field(row)
                                    : row[col.field === void 0 ? col.name : col.field],
                                col.format
                            )
                        )
                        .join(',')
                )
            )
            .join('\r\n');

        const status = exportFile(name, content, 'text/csv');

        if (status !== true) {
            console.log('download fail');
            //   $q.notify({
            //     message: 'Browser denied file download...',
            //     color: 'negative',
            //     icon: 'warning'
            //   })
        }
    },
    random() {
        return Math.random().toString(36).slice(2);
    },
    processcolumn(exampleitem) {
        console.log('exampleitem', exampleitem);
        let keylist = Object.keys(exampleitem);
        console.log('keylist', keylist);
        let columns = [];
        keylist.forEach((item) => {
            let name = item;
            let label = item.replace('_', ' ').toUpperCase();
            let col = {
                name: name,
                label: label,
                align: 'center',
                field: name,
            };
            columns.push(col);
        });
        return columns;
    },
    timeStamp() {
        return Math.floor(Date.now() / 1000);
    },
    async hasInternet(url) {
        try {
            await fetch(url);
            return true;
        } catch (error) {
            return false;
        }
    },
    construct_sentences(start_time, end_time, limit) {
        const minute = 60;
        const hour = 60 * minute;
        const day = 24 * hour;
        const week = 7 * day;
        const month = 4 * week;

        const duration = end_time - start_time;
        const withinLimit = limit ? duration <= limit : true;
        let summary = '';
        if (end_time > 0) {
            if (duration < minute) {
                summary = `${duration} minutes.`;
            } else if (duration < hour) {
                const hours = Math.floor(duration / minute);
                summary = `${hours} hour(s)`;
            } else if (duration < day) {
                const hours = Math.floor(duration / hour);
                summary = `${hours} hour(s)`;
            } else if (duration < week) {
                const days = Math.floor(duration / day);
                summary = `${days} day(s)`;
            } else if (duration < month) {
                const weeks = Math.floor(duration / week);
                summary = `${weeks} week(s) `;
            } else {
                const months = Math.floor(duration / month);
                summary = `${months} month(s)`;
            }
        } else summary = 'Not yet.';
        let finaldata = { withinLimit, summary };
        return finaldata;
    },
};

export default {
    fn,
};
