
package com.twitter.postmortem.handler;

import java.util.concurrent.atomic.AtomicLong;
import java.util.logging.Logger;

import javax.ws.rs.POST;
import javax.ws.rs.Path;

import com.google.inject.Inject;

import com.twitter.common.stats.Stats;

@Path("/write")
public class WriteHandler {
  private static final Logger LOG = Logger.getLogger(ReadHandler.class.getName());
  private static final AtomicLong WRITES = Stats.exportLong("writes");

  @Inject
  WriteHandler() {
  }

  /**
   * Services an incoming write request.
   */
  @POST
  @Path("/write")
  public String writeData() {
    WRITES.incrementAndGet();
    LOG.info("Writing data!");
    //TODO(jsmith): Write to whatever datastore we use
    return "\n";
  }
}
