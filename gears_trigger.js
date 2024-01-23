#!js name=StreamTrigger1 api_version=1.0
redis.registerStreamTrigger(
    "consumer", // consumer name
    "stream", // streams prefix
    function(c, data) {
        // callback to run on each element added to the stream
        val = JSON.stringify(data, (key, value) =>
            typeof value === 'bigint'
                ? value.toString()
                : value // return everything else unchanged
        );
        var curr_time = c.call("time")[0];

        c.call('set','hello:skr', val);

    }
);