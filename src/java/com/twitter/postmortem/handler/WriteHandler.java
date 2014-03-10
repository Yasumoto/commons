package com.twitter.postmortem.handler;

import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

import javax.ws.rs.POST;
import javax.ws.rs.Path;

import com.google.common.base.Preconditions;
import com.google.inject.Inject;

import com.twitter.common.base.Function;
import com.twitter.common.stats.Stats;

@Path("/write")
public class WriteHandler {
  private static final Logger LOG = Logger.getLogger(ReadHandler.class.getName());
  private static final AtomicLong WRITES = Stats.exportLong("writes");

  private final Function<String, String> datastore;

  @Inject
  WriteHandler(Function<String, String> datastore) {
    this.datastore = Preconditions.checkNotNull(datastore);
  }

  /**
   * Services an incoming write request.
   */
  @POST
  @Path("")
  public String writeData(String data) {
    WRITES.incrementAndGet();
    LOG.info("Writing data from the POST request: " + data);
    return datastore.apply(data);
  }
}
