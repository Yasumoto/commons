package com.twitter.postmortem.handler;

import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;

import com.google.inject.Inject;

import com.twitter.common.stats.Stats;

@Path("/read")
public class ReadHandler {
  private static final Logger LOG = Logger.getLogger(ReadHandler.class.getName());
  private static final AtomicLong READS = Stats.exportLong("reads");

  @Inject
  ReadHandler() {
  }

  /**
   * Services an incoming read request for matching messages.
   */
  @GET
  @Path("/{message}")
  public String readData(@PathParam("message") final String message) {
    READS.incrementAndGet();
    LOG.info("Reading data: " + message);
    //TODO(jsmith): Read from watever datastore we use
    return "holy sweet jimsus\n" + message;
  }
}
