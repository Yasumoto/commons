package com.twitter.postmortem.handler;

import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;

import com.google.common.base.Preconditions;
import com.google.inject.Inject;

import com.twitter.common.base.Function;
import com.twitter.common.stats.Stats;

@Path("/read")
public class ReadHandler {
  private static final Logger LOG = Logger.getLogger(ReadHandler.class.getName());
  private static final AtomicLong READS = Stats.exportLong("reads");

  private final Function<String, String> datastore;

  @Inject
  ReadHandler(Function<String, String> datastore) {
    this.datastore = Preconditions.checkNotNull(datastore);
  }

  /**
   * Services an incoming read request for matching messages.
   */
  @GET
  @Path("/{message}")
  public String readData(@PathParam("message") final String message) {
    READS.incrementAndGet();
    LOG.info("Finding messages that match: " + message);
    //TODO(jsmith): Actually match data before returning it
    return datastore.apply("");
  }
}
